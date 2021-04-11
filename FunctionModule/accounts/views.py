from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from FunctionModule.contacts.models import Contact
from django.contrib.admin import site

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
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
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

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'Bạn đã đăng nhập thành công')
      return redirect('dashboard')
    else:
      messages.error(request, 'Thông tin không hợp lệ')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'Bạn đã đăng xuất')
    return redirect('index')

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

  context = {
    'contacts': user_contacts
  }
  return render(request, 'accounts/dashboard.html', context)