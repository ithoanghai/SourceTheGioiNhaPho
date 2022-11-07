from FunctionModule import admin_site
from django.core.files.uploadedfile import UploadedFile

from .forms import ImportRealtorForm
from .import_realtor import handle_import
from .models import Realtor
from django.http import HttpRequest, JsonResponse, HttpResponse

from ..admin_site.filters import ChoicesFieldListFilter, RangeNumericFilter
from ..admin_site import BooleanFieldListFilter, DateFieldListFilter
from ..customers.models import Customer
from ..listings.models import ListingHistory, Listing
from ..transactions.models import Transaction, TransactionHistory


class ListingInline(admin_site.TabularInline):
    model = Listing
    max_num = 10
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created','date_update', 'status', 'address', 'area','floors', 'price', )


class ListingHistoryInline(admin_site.TabularInline):
    model = ListingHistory
    max_num = 10
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date_created', 'area','floors', 'price', 'warehouse', )


class CustomerInline(admin_site.TabularInline):
    model = Customer
    max_num = 10
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('hire_date', 'custormer_type', 'transactionStatus', 'name', 'phone', 'district', 'financial_range', )


class TransactionInline(admin_site.TabularInline):
    model = Transaction
    max_num = 10
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'status', 'trantype', 'request_price', 'customer',)


class TransactionHistoryInline(admin_site.TabularInline):
    model = TransactionHistory
    max_num = 10
    extra = 0  # If you have a fixed number number of answers, set it here.
    fields = ('date', 'transaction', 'status', 'reason', 'comment',  'realtor', )


class RealtorAdmin(admin_site.ModelAdmin):
    list_display = ('name', 'position', 'phone1', 'countryside', 'department', 'work_area','is_cooperate','status','is_published', 'facebook')
    list_display_links = ('name',)
    search_fields = ('id', 'name','phone1','phone2', 'email', 'address','title','birthyear','identifier', 'position', 'countryside', 'workplace', 'department', 'work_area', 'facebook','referral', 'hire_date')
    autocomplete_fields = ['user']
    list_per_page = 200
    ordering = ('name', '-hire_date')
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
    inlines = [TransactionInline, TransactionHistoryInline, CustomerInline, ListingInline, ListingHistoryInline,  ]

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
