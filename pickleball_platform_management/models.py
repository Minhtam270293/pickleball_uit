from django.db import models

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class NguoiDung(models.Model):
    ho_ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(
        max_length=15,
        unique=True,
        blank=True, null=False,
        validators=[
            RegexValidator(
                regex=r'^0\d{9,10}$',
                message='Số điện thoại phải bắt đầu bằng 0 và có 10-11 chữ số'
            )
        ]
    )
    ngay_sinh = models.DateField(blank=True, null=True)
    gioi_tinh = models.CharField(
        max_length=10,
        choices=[('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác')],
        blank=True, null=True
    )
    vai_tro = models.CharField(
        max_length=20,
        default='nguoi_dung'
    )
    ngay_dang_ky = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ho_ten

class San(models.Model):
    ten_san = models.CharField(max_length=100)
    dia_diem = models.CharField(max_length=255, unique=True)
    gia_thue_theo_gio = models.DecimalField(max_digits=10, decimal_places=2)
    mo_ta = models.TextField(blank=True, null=True)
    so_san_con = models.PositiveIntegerField()
    gio_mo_cua = models.TimeField()
    gio_dong_cua = models.TimeField()
    doanh_thu = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def clean(self):
        if self.gio_mo_cua >= self.gio_dong_cua:
            raise ValidationError("Giờ mở cửa phải trước giờ đóng cửa.")

    def __str__(self):
        return self.ten_san

class DanhGiaSan(models.Model):
    diem = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )
    noi_dung = models.TextField(max_length=200)
    ngay_danh_gia = models.DateTimeField(auto_now_add=True)
    san_id = models.ForeignKey('San', on_delete=models.CASCADE, related_name='danh_gias')
    nguoi_dung_id = models.ForeignKey('NguoiDung', on_delete=models.CASCADE, related_name='danh_gias')

    def clean(self):
        da_dat_san = DatSan.objects.filter(
            san_id=self.san_id,
            nguoi_dung_id=self.nguoi_dung_id
        ).exists()
        if not da_dat_san:
            raise ValidationError("Người dùng chỉ được đánh giá sân mà họ đã đặt.")    

    def __str__(self):
        return f"{self.san_id.ten_san} - {self.nguoi_dung_id.ho_ten} ({self.diem}★)"
    
class HuongDan(models.Model):
    tieu_de = models.CharField(max_length=200, unique=True)
    thoi_gian_tao = models.DateTimeField(auto_now_add=True)
    noi_dung = models.TextField()
    nguoi_tao = models.ForeignKey('NguoiDung', on_delete=models.CASCADE, related_name='huong_dans')
    cap_do = models.CharField(
        max_length=20,
        choices=[('de', 'Dễ'), ('trung binh', 'Trung bình'), ('kho', 'Khó')],
        blank=True,
        null=True
    )

    def __str__(self):
        return self.tieu_de
    
class DatSan(models.Model):
    thoi_gian_dat = models.DateTimeField(auto_now_add=True)
    thoi_gian_bat_dau = models.TimeField()
    thoi_gian_ket_thuc = models.TimeField()
    san_id = models.ForeignKey('San', on_delete=models.CASCADE, related_name='dat_sans')
    nguoi_dung_id = models.ForeignKey('NguoiDung', on_delete=models.CASCADE, related_name='dat_sans')
    so_luong_san = models.PositiveIntegerField()
    tong_tien = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.thoi_gian_bat_dau >= self.thoi_gian_ket_thuc:
            raise ValidationError("Thời gian bắt đầu phải trước thời gian kết thúc.")
        if self.san_id:
            if self.thoi_gian_bat_dau < self.san_id.gio_mo_cua or self.thoi_gian_ket_thuc > self.san_id.gio_dong_cua:
                raise ValidationError("Thời gian đặt phải nằm trong giờ mở cửa và đóng cửa của sân.")
            if self.so_luong_san > self.san_id.so_san_con:
                raise ValidationError("Số lượng sân đặt vượt quá số sân còn lại.")

    def __str__(self):
        return f"Đặt sân {self.san_id.ten_san} bởi {self.nguoi_dung_id.ho_ten} ({self.thoi_gian_dat})"