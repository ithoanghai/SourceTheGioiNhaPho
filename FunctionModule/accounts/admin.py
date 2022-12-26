from django.contrib import messages, admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .forms import UserChangeForm
from .models import User
from TownhouseWorldRealestate.filters import ChoicesFieldListFilter, BooleanFieldListFilter, DateFieldListFilter
from ..blog.models import Post
from ..customers.models import Customer
from ..listings.models import Listing, ListingHistory
from ..transactions.models import Transaction


class BlogInline(admin.TabularInline):
    model = Post
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created','date_update', 'title', )


class ListingHistoryInline(admin.TabularInline):
    model = ListingHistory
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created', 'area','floors', 'price', 'warehouse', )


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('hire_date', 'custormer_type', 'transactionStatus', 'name', 'phone', 'district', 'financial_range', )


class ListingInline(admin.TabularInline):
    model = Listing
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created','date_update', 'status', 'address', 'area','floors', 'price', )


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'status', 'trantype', 'request_price','listing','customer', 'realtor',)


class AccountAdmin(AuthUserAdmin):
    form = UserChangeForm
    add_fieldsets = (
        ('THÔNG TIN CƠ BẢN', {
            'classes': ('wide',),
            'fields': (('username','first_name', 'last_name'),('password1', 'password2'), ('phone','email')),
        }), ('THÔNG TIN BỔ SUNG', {'fields': (
            ('address', 'dob', 'gender'),
            ('avatar', 'bio',),
            ('is_broker', 'is_investor',))})
    )

    fieldsets = (
        ('THÔNG TIN CƠ BẢN', {
            'classes': ('wide',),
            'fields': (('username', 'password'), ('phone', 'email'))}),
        ('THÔNG TIN BỔ SUNG', {'fields': (
            ('first_name', 'last_name'),
            ('address', 'dob', 'gender'),
            ('avatar', 'bio'), ('is_broker', 'is_investor',))}),
        ('PHÂN QUYỀN SỬ DỤNG', {
            'fields': (('is_active', 'is_staff', 'is_superuser'), ('groups', 'user_permissions'))
        }),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': (('first_time','last_login'), 'date_joined')}),
    )
    list_display = ('id','username', 'name', 'phone', 'email', 'joined_date', 'is_staff', 'is_broker', 'is_investor', 'is_active')
    list_display_links = ('name', 'phone')
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    #list_filter = ('date_joined', 'is_broker', 'is_investor', 'is_staff', 'is_active')
    list_filter = (
        ('date_joined', DateFieldListFilter),
        ('last_login', DateFieldListFilter),
        ('dob', DateFieldListFilter),
        ('gender', ChoicesFieldListFilter),
        ('is_broker', BooleanFieldListFilter),
        ('is_investor', BooleanFieldListFilter),
        ('is_staff', BooleanFieldListFilter),
        ('is_superuser', BooleanFieldListFilter),
        ('is_active', BooleanFieldListFilter),
    )
    list_per_page = 100
    readonly_fields = [
        'date_joined', 'user_image',
    ]
    list_editable = ('is_staff', 'is_active',)
    ordering = ('first_name', 'last_name', 'date_joined', )
    filter_horizontal = ('groups', 'user_permissions')
    inlines = [CustomerInline, BlogInline, ListingHistoryInline, ]

    # change_list_template = 'admin/auth/user/change_list.html'
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(id=request.user.id)


class GroupAdmin(admin.ModelAdmin):
    verbose_name = "Quản trị nhóm người dùng"
    Group._meta.get_field('name').verbose_name = 'Tên nhóm'
    Group._meta.get_field('permissions').verbose_name = 'Quyền sử dụng'
    Group._meta.verbose_name = "Nhóm Người dùng"
    Group._meta.verbose_name_plural = "Nhóm Người dùng"


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'content_type', 'codename')
    ordering = ('content_type','name')
    verbose_name = "Quản trị Quyền người dùng"
    Permission._meta.get_field('name').verbose_name = 'Tên quyền'
    Permission._meta.get_field('content_type').verbose_name = 'Module chức năng'
    Permission._meta.get_field('codename').verbose_name = 'Mã chức năng'
    Permission._meta.verbose_name = 'Quyền Người dùng'
    Permission._meta.verbose_name_plural = 'Quyền Người dùng'

admin.site.register(Permission, PermissionAdmin)
#admin.site.register(ContentType)
#admin.site.register(Group, GroupAdmin)
admin.site.register(User, AccountAdmin)
#admin.site.unregister(TokenProxy)
#admin.site.unregister(SocialToken)
#admin.site.unregister(EmailAddress)
