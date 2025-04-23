from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HuongDanChoi(models.Model):
    tieu_de = models.CharField(max_length=200)
    nguoi_tao = models.ForeignKey(User, on_delete=models.CASCADE)
    thoi_gian_tao = models.DateTimeField(auto_now_add=True)
    noi_dung = models.TextField()

    def __str__(self):
        return self.tieu_de

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure tieu_de is not empty
        if not self.tieu_de.strip():
            raise ValidationError('Tiêu đề không được để trống')
        
        # Ensure tieu_de has minimum length
        if len(self.tieu_de.strip()) < 5:
            raise ValidationError('Tiêu đề phải có ít nhất 5 ký tự')
        
        # Ensure noi_dung is not empty
        if not self.noi_dung.strip():
            raise ValidationError('Nội dung không được để trống')
        
        # Ensure noi_dung has minimum length
        if len(self.noi_dung.strip()) < 20:
            raise ValidationError('Nội dung phải có ít nhất 20 ký tự')
