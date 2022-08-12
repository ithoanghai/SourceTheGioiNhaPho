from django.contrib import admin
from django.core.files.uploadedfile import UploadedFile

from .forms import ImportRealtorForm
from .import_realtor import handle_import
from .models import Realtor
from django.http import HttpRequest, JsonResponse

from ..filters import DropdownFilter, DateFieldFilter, BooleanFieldFilter


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthyear', 'position', 'phone1', 'countryside', 'department', 'work_area','is_cooperate','is_published','email', 'facebook')
    list_display_links = ('name',)
    search_fields = ('id', 'name','phone1','phone2', 'email', 'birthyear', 'position', 'countryside', 'workplace', 'department', 'work_area', 'facebook', 'hire_date')
    autocomplete_fields = ['user']
    list_per_page = 200
    ordering = ('name', 'hire_date')
    #filter_vertical = ('user',)
    list_editable = ('email','is_cooperate','is_published',)
    list_filter = (
        ('position', DropdownFilter),
        ('workplace', DropdownFilter),
        ('birthyear', DropdownFilter),
        ('is_cooperate', BooleanFieldFilter),
        ('is_published', BooleanFieldFilter),
        ('hire_date', DateFieldFilter),
    )
    readonly_fields = []
    add_fieldsets = (
        ('THÔNG TIN CƠ BẢN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': ('user', ( 'name', 'birthyear', 'position'), ('countryside', 'address'), ('phone1', 'phone2','email')),
        }), ('THÔNG TIN BỔ SUNG', {'fields': (
            ('workplace', 'department', 'work_area'),
            'facebook', 'story',)})
    )

    fieldsets = (
        ('THÔNG TIN CƠ BẢN CHUYÊN VIÊN', {
            'classes': ('wide',),
            'fields': ('user', ('name', 'birthyear', 'position'), ('countryside', 'address'), ('phone1', 'phone2', 'email')),
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


@admin.site.register_view('realtors/realtor/import-export')
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


admin.site.register(Realtor, RealtorAdmin)
