from django.contrib import messages, auth
from django.contrib.admin import site
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.shortcuts import render, redirect
from allauth.account.views import get_adapter

from FunctionModule.accounts.models import User
from FunctionModule.contacts.models import Contact
from FunctionModule.accounts.forms import UserRegisterForm


def register(request):
    if request.method == "GET":
        return render(
            request, "accounts/_register.html",
            {"form": UserRegisterForm}
        )
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST or None)

        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        reg_user = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'phone': phone,
            'email': email,
            'password': password,
            'password2': password2
        }

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Người dùng đã được sử dụng trên hệ thống')

        # Check username
        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'Số điện thoại này đã được sử dụng trên hệ thống')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email đã được sử dụng trên hệ thống')

            # Check if passwords match
        if password != password2:
            messages.error(request, 'Mật khẩu không trùng khớps')

        if form.is_valid():
            # Looks good
            # user = User.objects.create_user(username=username, password=password, email=email,
            #                                first_name=first_name, last_name=last_name)
            user = form.save()
            user_password = form.cleaned_data.get('password')
            user.set_password(user_password)
            user.save()
            messages.success(request,
                             'Bạn đã đăng ký người dùng thành công và có thể đăng nhập. Để sử dụng các tính năng của chuyên viên TGNP, bạn cần liên hệ với admin để đươc cấp quyền.')
            return redirect('login')

        return render(request, 'accounts/_register.html', {'reg_user': reg_user, 'form': form})

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/_register.html')


def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            query = Q(username=username) | Q(email=username)
            user = User.objects.get(query)
            adapter = get_adapter(request)

            if user is not None:
                is_correct = user.check_password(password)
                if not is_correct:
                    messages.error(request, 'Thông tin đăng nhập không hợp lệ')

                adapter.login(request, user)
                messages.success(request, 'Bạn đã đăng nhập thành công')
            else:
                messages.error(request, 'Người dùng không tồn tại')

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            messages.success(request, 'Xuất hiện lỗi khi đăng nhập, bạn cần liên hệ quản trị viên')

        return redirect('index')
    else:
        messages.error(request, 'Bạn cần gửi đủ thông tin đăng nhập')
        return redirect('/admin/')


def logout_handler(request):
    if request.user is not None:
        auth.logout(request)
        if request.user.is_staff or request.user.is_superuser:
            messages.success(request, 'Bạn vừa đăng xuất, cảm ơn bạn đã hợp tác nhiệt tình với TGNP!')
        else:
            auth.logout(request)
            messages.success(request, 'Bạn vừa đăng xuất')

        return render(request, 'admin/includes/_logged_out.html')


def profile(request):
    app_list = site.get_app_list(request)
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts,
        'available_apps': app_list
    }
    if request.user.is_authenticated:
        return render(request, 'accounts/_profile.html', context)
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
