import datetime
import urllib
from email.charset import BASE64

from django.contrib import messages, auth
from django.contrib.admin import site
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from allauth.account.views import get_adapter
from gevent import os
import json

from FunctionModule.accounts.auth import RealEstateAuthBackend
from FunctionModule.accounts.models import User, Point
from FunctionModule.accounts.forms import UserRegisterForm, UserProfileForm
from FunctionModule.transactions.models import Transaction
from FunctionModule.zalo.app import ZaloAppInfo, Zalo3rdAppClient
from FunctionModule.zalo.oa import ZaloOaClient
from TownhouseWorldRealestate.settings import MEDIA_ROOT, ZALO_APP_ID, ZALO_APP_CALLBACK_URL, ZALO_CODE_CHALLENGE, \
    ZALO_STATE, ZALO_APP_SECRET, ZALO_REFRESH_TOKEN


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
        if request.POST.get('is_broker') == 'on':
            is_broker = True
        else:
            is_broker = False
        if request.POST.get('is_investor') == 'on':
            is_investor = True
        else:
            is_investor = False
        reg_user = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'phone': phone,
            'email': email,
            'password': password,
            'password2': password2,
            'is_broker': is_broker,
            'is_investor': is_investor
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
            messages.error(request, 'Mật khẩu không trùng khớp')

        if form.is_valid() and form.cleaned_data:
            # Looks good
            # user = User.objects.create_user(username=username, password=password, email=email,
            #                                first_name=first_name, last_name=last_name)
            user = form.save()
            user_password = form.cleaned_data.get('password')
            user.set_password(user_password)
            user.save()
            Point.objects.create_base(user__id=user.id, investment_point=0, investment_account=0, prestige_points=1, potential_points=1, bds_referral_point=0, customer_referral_point=0)
            messages.success(request,
                             'Bạn đã đăng ký người dùng thành công và có thể đăng nhập. (chú ý: Để trở thành Chuyên viên và sử dụng các tính năng của Chuyên viên TGNP, bạn cần liên hệ với admin.)')
            return redirect('register_success')
        else:
            messages.error(request,'Đã xảy ra lỗi. Bạn đăng ký chưa được!')

            return render(request, 'accounts/_register.html', {'reg_user': reg_user, 'form': form})

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/_register.html')


def register_success(request):
    return render(request, 'accounts/_registerSuccess.html')


def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            query = Q(username=username) | Q(phone=username) | Q(email=username)
            user = User.objects.get(query)
            adapter = get_adapter(request)

            if user is not None:
                is_correct = user.check_password(password)
                if not is_correct:
                    messages.error(request, 'Thông tin đăng nhập không hợp lệ')

                adapter.login(request, user)
                messages.success(request, 'Bạn đã đăng nhập thành công')
                return redirect('index')
            else:
                messages.error(request, 'Người dùng không tồn tại')
                return render(request, 'accounts/_logged_out.html')

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            messages.success(request, 'Xuất hiện lỗi khi đăng nhập, bạn cần liên hệ quản trị viên')
            return render(request, 'accounts/_logged_out.html')

    else:
        return redirect('/admin/')


def logout_handler(request):
    if request.user is not None:
        auth.logout(request)
        if request.user.is_staff or request.user.is_superuser:
            messages.success(request, 'Bạn vừa đăng xuất, cảm ơn bạn đã hợp tác nhiệt tình với TGNP!')
        else:
            auth.logout(request)
            messages.success(request, 'Bạn vừa đăng xuất')

        return render(request, 'accounts/_logged_out.html')


def profile(request):
    app_list = site.get_app_list(request)

    if request.user.is_authenticated:
        if request.method == 'GET':
            trans = Transaction.objects.filter(user=request.user).order_by('-date')
            point = Point.objects.filter(user=request.user).first()
            paginator = Paginator(trans, 10)
            page = request.GET.get('page')
            paged_trans = paginator.get_page(page)
            context = {
                'transactions': paged_trans,
                'point': point,
            }

            return render(request, 'accounts/_profile.html', context)

        elif request.method == 'POST':
            form = UserProfileForm(request.POST or None, request.FILES, instance=request.user)
            # Get form values
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            phone = request.POST['phone']
            email = request.POST['email']
            dob = request.POST['dob']
            gender = request.POST['gender']
            address = request.POST['address']
            if request.POST.get('is_broker') == 'on':
                is_broker = True
            else:
                is_broker = False
            if request.POST.get('is_investor') == 'on':
                is_investor = True
            else:
                is_investor = False
            bio = request.POST['bio']
            if request.FILES.get('avatar', None) is not None:
                avatar = request.FILES.get('avatar')
            else:
                avatar = request.POST['avatar']
            reg_user = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'phone': phone,
                'email': email,
                'dob': dob,
                'gender': gender,
                'address': address,
                'is_broker': is_broker,
                'is_investor': is_investor,
                'bio': bio,
                'avatar': avatar,
            }

            if form.is_valid() and form.cleaned_data:
                # Looks good
                # user = User.objects.create_user(username=username, password=password, email=email,
                #                                first_name=first_name, last_name=last_name)

                if request.FILES.get('avatar', None) is not None and form.is_multipart():
                    try:
                        save_file(avatar)
                        os.remove(request.user.avatar.url)
                    except Exception as e:
                        print('Exception in removing old profile image: ', e)
                    request.user.avatar = request.FILES['avatar']
                    request.user.save()
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Bạn đã lưu thông tin thành công')

                return redirect('profile')

            return render(request, 'accounts/_profile.html', {'reg_user': reg_user, 'form': form})
    else:
        return render(request, 'accounts/_profile.html')


def save_file(file, path=''):
    ''' Little helper to save a file
    '''
    filename = file._get_name()
    fd = open('%s/photos/%Y%m%d/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return filename


def password_change(request):
    form = PasswordChangeForm(request.user, request.POST)
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list,
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Mật khẩu của bạn đã được thay đổi, cập nhật thành công!')
            return redirect('profile')
        else:
            messages.error(request, 'Hãy hoàn thành các lỗi ở dưới.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', context)


def social_login_cancelled(request):
    messages.warning(request, 'Bạn đã hủy đăng nhập. Xin đăng nhập lại.')
    return redirect('/')


def login_zalo_callback(request):
    try:
        # user id Hải user_id	8748099517921268204
        zalo_info = ZaloAppInfo.ZaloAppInfo(app_id=ZALO_APP_ID, secret_key=ZALO_APP_SECRET, callback_url=ZALO_APP_CALLBACK_URL)
        zalo_3rd_app_client = Zalo3rdAppClient.Zalo3rdAppClient(zalo_info)
        #authorization_code = "https://oauth.zaloapp.com/v4/permission?app_id=%d&redirect_uri=%s&code_challenge=%s&state=%s" %(zalo_info.app_id, zalo_info.callback_url, ZALO_CODE_CHALLENGE,'yes')
        #print(authorization_code)
        login_url = zalo_3rd_app_client.get_login_url()
        profile = zalo_3rd_app_client.get('/me', ZALO_REFRESH_TOKEN, {'fields': 'id, name, birthday, gender, picture, phone'})
        print(profile)
        if profile is not None:
            user = User()
            user.first_name = profile["name"]
            user.username = profile["id"]
            user.set_password(user.username)
            user.phone = profile["id"]
            cr_date = profile["birthday"]
            cr_date = datetime.datetime.strptime(cr_date, '%d/%m/%Y')
            user.dob = cr_date.strftime("%Y-%m-%d")
            user.gender = profile["gender"]
            picture = profile["picture"]
            #avatar = json.loads(picture)
            #print(avatar)

            user_check = User.objects.filter(username=user.username).first()
            if user_check is None:
                user.save()
            else:
                user = user_check
            adapter = get_adapter(request)
            adapter.login(request, user)
            messages.success(request, 'Bạn đã đăng nhập thành công')

        return redirect('index')

    except (ObjectDoesNotExist, MultipleObjectsReturned):
        messages.error(request, 'Xuất hiện lỗi khi đăng nhập, bạn cần liên hệ quản trị viên')
        return redirect('login')
