from FunctionModule import admin_site
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Q

from .forms import ImportRealtorForm
from .import_realtor import handle_import
from .models import Realtor
from django.http import HttpRequest, JsonResponse, HttpResponse

from ..admin_site.filters import ChoicesFieldListFilter, RangeNumericFilter
from ..admin_site import BooleanFieldListFilter, DateFieldListFilter
from ..customers.models import Customer
from ..listings import TransactionType, Status
from ..listings.models import ListingHistory, Listing
from ..transactions.models import Transaction, TransactionHistory


class ListingInline(admin_site.TabularInline):
    model = Listing
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created','date_update', 'status', 'address', 'area','floors', 'price','is_published' )
    show_change_link = True
    verbose_name = "BẤT ĐỘNG SẢN CẦN QUẢN LÝ"
    verbose_name_plural = "20 BĐS CŨ NHẤT CỦA CHUYÊN VIÊN CÒN GIAO DỊCH"

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        LIMIT_SEARCH = 20
        queryset = super(ListingInline, self).get_queryset(request)
        ids = queryset.order_by('date_created').values('pk')[:LIMIT_SEARCH]
        qs = Listing.objects.filter(~Q(status=Status.SOLD),pk__in=ids).order_by('date_created')
        #return qs.filter(user=request.user)
        return qs


class CustomerInline(admin_site.TabularInline):
    model = Customer
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('hire_date','financial_range',  'custormer_type', 'transactionStatus', 'name', 'phone', 'district', )
    show_change_link = True
    verbose_name = "KHÁCH HÀNG CẦN QUẢN LÝ"
    verbose_name_plural = "DS KHÁCH HÀNG CẦN CHĂM SÓC"

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        LIMIT_SEARCH = 20
        queryset = super(CustomerInline, self).get_queryset(request)
        ids = queryset.order_by('-financial_range').values('pk')[:LIMIT_SEARCH]
        qs = Customer.objects.filter(pk__in=ids).order_by('-financial_range')
        # return qs.filter(user=request.user)
        return qs


class TransactionInline(admin_site.TabularInline):
    model = Transaction
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'status', 'trantype', 'message', 'request_price', 'customer',)
    verbose_name = "GIAO DỊCH LIÊN QUAN"
    verbose_name_plural = "GIAO DỊCH ĐƯỢC GIAO QUẢN LÝ"
    readonly_fields = ('status', 'trantype', 'message', 'request_price', 'customer',)
    can_delete = False

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        LIMIT_SEARCH = 20
        queryset = super(TransactionInline, self).get_queryset(request)
        ids = queryset.order_by('-date').values('pk')[:LIMIT_SEARCH]
        qs = Transaction.objects.filter(pk__in=ids).order_by('-date')
        # return qs.filter(user=request.user)
        return qs


class TransactionHistoryInline(admin_site.TabularInline):
    model = TransactionHistory
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'status', 'transaction', 'reason', 'comment',  'realtor', )
    verbose_name = "XỬ LÝ GIAO DỊCH"
    verbose_name_plural = "XỬ LÝ GIAO DỊCH"
    show_change_link = True
    readonly_fields = ()
    can_delete = False

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        LIMIT_SEARCH = 20
        queryset = super(TransactionHistoryInline, self).get_queryset(request)
        ids = queryset.order_by('-date').values('pk')[:LIMIT_SEARCH]
        qs = TransactionHistory.objects.filter(pk__in=ids).order_by('-date')
        # return qs.filter(user=request.user)
        return qs


class RealtorAdmin(admin_site.ModelAdmin):
    list_display = ('name', 'position', 'phone1', 'department', 'work_area','is_cooperate','status','is_published', 'facebook')
    list_display_links = ('name',)
    search_fields = ('id', 'name','phone1','phone2', 'email', 'address','title','birthyear','identifier', 'position', 'countryside', 'workplace', 'department', 'work_area', 'facebook','referral', 'hire_date')
    autocomplete_fields = ['user']
    list_per_page = 100
    ordering = ('-name', '-hire_date')
    #filter_vertical = ('user',)
    list_editable = ('email','is_cooperate','is_published',)
    list_filter = (
        ('position', ChoicesFieldListFilter),
        ('workplace', ChoicesFieldListFilter),
        ('is_cooperate', BooleanFieldListFilter),
        ('is_published', BooleanFieldListFilter),
        ('status', ChoicesFieldListFilter),
        ('hire_date', DateFieldListFilter),
        ('birthyear', RangeNumericFilter),
        ('level', RangeNumericFilter),
    )
    readonly_fields = []
    inlines = [CustomerInline, ListingInline, TransactionInline, TransactionHistoryInline,   ]

    add_fieldsets = (
        ('THÔNG TIN CƠ BẢN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': ('user', ( 'name', 'birthyear', 'position'), ('avatar', 'countryside', 'address'), ('phone1', 'phone2','email')),
        }), ('THÔNG TIN BỔ SUNG', {'fields': (
            ('workplace', 'department', 'work_area'),
            'facebook', 'story',)})
    )

    fieldsets = (
        ('THÔNG TIN CƠ BẢN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': ('user', ('name', 'birthyear', 'position'), ('avatar','countryside', 'address'), ('phone1', 'phone2', 'email')),
        }),
        ('THÔNG TIN BỔ SUNG', {'fields': (
            ('workplace', 'department', 'work_area'),
            ('facebook', 'website', 'youtube'),
            ('title', 'level', 'training'),
            ('referral', 'story'))}),
        ('THÔNG TIN KHÁC', {
            'fields': (('status', 'is_cooperate', 'is_published'),)
        }),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': (('date_join', 'hire_date'),)}),
    )

    class Media:
        js = ('admin/js/dropzone.js', 'admin/js/realtor.js', 'admin/js/filepond-4.28.2.min.js',
              'admin/js/micromodal-0.4.6.min.js')
        css = {
            'all': ('admin/css/dropzone.css', 'admin/css/listing.css', 'admin/css/filepond.min.css')
        }

    def changelist_view(
        self,
        request: HttpRequest,
        form_url: str = '',
        extra_context: dict = None
    ) -> HttpResponse:

        extra_context = extra_context or {}
        extra_context.update({
            'extrabutton': True,
        })
        return super().changelist_view(request, extra_context=extra_context)


@admin_site.site.register_view('realtors/realtor/import-export')
def import_csv_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        form = ImportRealtorForm(request.POST or None, request.FILES)
        if form.is_valid():
            file: UploadedFile = form.cleaned_data.get('file')

            handle_import(request, f'media/import-export/{file}')

            return JsonResponse({})
        else:
            return JsonResponse({'status': 'error', 'message': str(form.errors)}, status=400)
    return JsonResponse({})


admin_site.site.register(Realtor, RealtorAdmin)
