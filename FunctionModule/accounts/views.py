from allauth.account.utils import get_login_redirect_url
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages, auth
from django.contrib.admin import site
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from allauth.account.views import get_adapter, _ajax_response

from FunctionModule.accounts import app_settings
from FunctionModule.accounts.models import User
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
                    'Bạn đã đăng ký người dùng thành công và có thể đăng nhập. (chú ý: Để trở thành Chuyên viên và sử dụng các tính năng của Chuyên viên TGNP, bạn cần liên hệ với admin.)')
            return redirect('register_success')

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

    context = {
        'available_apps': app_list
    }
    if request.user.is_authenticated:
        return render(request, 'accounts/_profile.html', context)
    else:
        return redirect('/admin/')


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


class AjaxCapableProcessFormViewMixin(object):
    def get(self, request, *args, **kwargs):
        response = super(AjaxCapableProcessFormViewMixin, self).get(
            request, *args, **kwargs
        )
        form = self.get_form()
        return _ajax_response(
            self.request, response, form=form, data=self._get_ajax_data_if()
        )

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            response = self.form_valid(form)
        else:
            response = self.form_invalid(form)
        return _ajax_response(
            self.request, response, form=form, data=self._get_ajax_data_if()
        )

    def get_form(self, form_class=None):
        form = getattr(self, "_cached_form", None)
        if form is None:
            form = super(AjaxCapableProcessFormViewMixin, self).get_form(form_class)
            self._cached_form = form
        return form

    def _get_ajax_data_if(self):
        return (
            self.get_ajax_data()
            if get_adapter(self.request).is_ajax(self.request)
            else None
        )

    def get_ajax_data(self):
        return None


class CloseableSignupMixin(object):
    template_name_signup_closed = (
        "account/signup_closed." + app_settings.TEMPLATE_EXTENSION
    )

    def dispatch(self, request, *args, **kwargs):
        try:
            if not self.is_open():
                return self.closed()
        except ImmediateHttpResponse as e:
            return e.response
        return super(CloseableSignupMixin, self).dispatch(request, *args, **kwargs)

    def is_open(self):
        return get_adapter(self.request).is_open_for_signup(self.request)

    def closed(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_signup_closed,
        }
        return self.response_class(**response_kwargs)


class RedirectAuthenticatedUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and app_settings.AUTHENTICATED_LOGIN_REDIRECTS:
            redirect_to = self.get_authenticated_redirect_url()
            response = HttpResponseRedirect(redirect_to)
            return _ajax_response(request, response)
        else:
            response = super(RedirectAuthenticatedUserMixin, self).dispatch(
                request, *args, **kwargs
            )
        return response

    def get_authenticated_redirect_url(self):
        redirect_field_name = self.redirect_field_name
        return get_login_redirect_url(
            self.request,
            url=self.get_success_url(),
            redirect_field_name=redirect_field_name,
        )