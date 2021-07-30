from django.contrib import messages, auth
from django.contrib.admin import site
from django.db.models import Q
from django.shortcuts import render, redirect
from allauth.account.views import get_adapter

from FunctionModule.accounts.models import User
from FunctionModule.contacts.models import Contact


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Tên người dùng đó đã được sử dụng')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email đã được sử dụng')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'Bạn đã đăng ký thành công và có thể đăng nhập')
                    return redirect('login')
        else:
            messages.error(request, 'Mật khẩu không phù hợp')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        query = Q(username=username) | Q(email=username)
        user = User.objects.get(query)
        adapter = get_adapter(request)

        if user is not None:
            is_correct = user.check_password(password)
            if not is_correct:
                messages.error(request, 'Thông tin không hợp lệ')
                return redirect('index')

            adapter.login(request, user)
            messages.success(request, 'Bạn đã đăng nhập thành công')
            return redirect('index')
        else:
            messages.error(request, 'Thông tin không hợp lệ')
            return redirect('index')
    else:
        messages.error(request, 'Bạn cần gửi đủ thông tin đăng nhập')
        return render(request, 'home/index.html')

def logout_handler(request):
        if request.user is not None and (request.user.is_staff or request.user.is_superuser):
            auth.logout(request)
            messages.success(request, 'Bạn vừa đăng xuất')
            return redirect('/admin/')
        else:
            auth.logout(request)
            messages.success(request, 'Bạn vừa đăng xuất')
            return redirect('index')

def profile(request):

    app_list = site.get_app_list(request)
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts,
        'available_apps': app_list
    }
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html', context)
    else:
        return redirect('/admin/')

def password_change(request):
    app_list = site.get_app_list(request)
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts,
        'available_apps': app_list
    }
    if request.user.is_authenticated:
        return render(request, 'accounts/change_password.html', context)
    else:
        return redirect('index')

def social_login_cancelled(request):
    messages.warning(request, 'Bạn đã hủy đăng nhập. Xin đăng nhập lại.')
    return redirect('/')
