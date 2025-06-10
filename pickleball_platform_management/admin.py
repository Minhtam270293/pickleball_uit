from django.contrib import admin
from .models import NguoiDung, San, DanhGiaSan, HuongDan, DatSan

@admin.register(NguoiDung)
class NguoiDungAdmin(admin.ModelAdmin):
    list_display = ['ho_ten', 'so_dien_thoai', 'ngay_sinh', 'gioi_tinh', 'vai_tro', 'ngay_dang_ky']
    search_fields = ['ho_ten', 'so_dien_thoai']

@admin.register(San)
class SanAdmin(admin.ModelAdmin):
    list_display = ['ten_san', 'dia_chi', 'gia_thue_theo_gio', 'so_san_con', 'gio_mo_cua', 'gio_dong_cua']
    search_fields = ['ten_san', 'dia_chi']

@admin.register(DanhGiaSan)
class DanhGiaSanAdmin(admin.ModelAdmin):
    list_display = ['san_id', 'nguoi_dung_id', 'diem', 'ngay_danh_gia']
    search_fields = ['san_id__ten_san', 'nguoi_dung_id__ho_ten']

@admin.register(HuongDan)
class HuongDanAdmin(admin.ModelAdmin):
    list_display = ['tieu_de', 'thoi_gian_tao', 'nguoi_tao', 'cap_do']
    search_fields = ['tieu_de', 'noi_dung', 'nguoi_tao__ho_ten']

@admin.register(DatSan)
class DatSanAdmin(admin.ModelAdmin):
    list_display = ['san_id', 'nguoi_dung_id', 'thoi_gian_dat', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'so_luong_san', 'tong_tien']
    search_fields = ['san_id__ten_san', 'nguoi_dung_id__ho_ten']

