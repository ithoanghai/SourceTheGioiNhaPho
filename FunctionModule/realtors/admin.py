from django.contrib import admin

from .models import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthyear', 'position', 'phone1', 'countryside', 'department', 'work_area', 'facebook')
    list_display_links = ('name',)
    search_fields = ('id', 'name', 'email', 'birthyear', 'position', 'countryside', 'workplace', 'department', 'work_area', 'facebook', 'hire_date')
    list_per_page = 200
    ordering = ('name', 'hire_date')
    filter_horizontal = ('user',)
    list_filter = ('position', 'workplace', 'title',  'hire_date')
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
            ('title','level',),
            'story')}),
        ('CÀI ĐẶT KHÁC', {
            'fields': (('is_cooperate', 'is_published'),)
        }),
        ('THỜI GIAN HOẠT ĐỘNG', {'fields': ('hire_date',)}),
    )


admin.site.register(Realtor, RealtorAdmin)
