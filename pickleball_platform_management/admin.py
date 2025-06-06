from django.contrib import admin
from .models import NguoiDung

@admin.register(NguoiDung)
class NguoiDungAdmin(admin.ModelAdmin):
    list_display = ['ho_ten', 'so_dien_thoai', 'ngay_sinh', 'gioi_tinh', 'vai_tro', 'ngay_dang_ky']
    search_fields = ['ho_ten', 'so_dien_thoai']

