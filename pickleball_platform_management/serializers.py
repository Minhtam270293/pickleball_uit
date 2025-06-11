from rest_framework import serializers
from .models import NguoiDung, San, DanhGiaSan, HuongDan, DatSan

class NguoiDungSerializer(serializers.ModelSerializer):
    ngay_sinh = serializers.DateField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'Ngày sinh phải đúng định dạng YYYY-MM-DD.'
        }
    )
    def validate_so_dien_thoai(self, value):
        if self.instance:
            if NguoiDung.objects.filter(so_dien_thoai=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Số điện thoại này đã được sử dụng.")
        else:
            if NguoiDung.objects.filter(so_dien_thoai=value).exists():
                raise serializers.ValidationError("Số điện thoại này đã được sử dụng.")
        return value

    class Meta:
        model = NguoiDung
        exclude = ['vai_tro']
        extra_kwargs = {
            'so_dien_thoai': {
                'error_messages': {
                    'unique': 'Số điện thoại này đã được sử dụng.'
                }
            }
        }

class SanSerializer(serializers.ModelSerializer):
    doanh_thu = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True, required=False)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.resolver_match and request.resolver_match.url_name != 'san-revenue':
            rep.pop('doanh_thu', None)
        return rep

    def validate(self, data):
        gio_mo_cua = data.get('gio_mo_cua')
        gio_dong_cua = data.get('gio_dong_cua')
        import datetime
        if gio_mo_cua is not None and gio_dong_cua is not None:
            if gio_mo_cua < datetime.time(5, 0) or gio_dong_cua > datetime.time(23, 0):
                raise serializers.ValidationError("Giờ hoạt động phải trong khoảng 5 giờ đến 23 giờ.")
            if gio_mo_cua >= gio_dong_cua:
                raise serializers.ValidationError("Giờ mở cửa phải trước giờ đóng cửa.")
        return data
    class Meta:
        model = San
        fields = '__all__'
        read_only_fields = ['doanh_thu']

class DanhGiaSanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaSan
        fields = '__all__'

    def validate(self, data):
        nguoi_dung = data.get('nguoi_dung_id')
        san = data.get('san_id')
        from .models import DatSan
        if not DatSan.objects.filter(nguoi_dung_id=nguoi_dung, san_id=san).exists():
            raise serializers.ValidationError("Người dùng chỉ được đánh giá sân mà họ đã đặt.")
        return data

class HuongDanSerializer(serializers.ModelSerializer):
    nguoi_tao_id = serializers.PrimaryKeyRelatedField(
        queryset=NguoiDung.objects.all(), source='nguoi_tao'
    )

    cap_do = serializers.ChoiceField(
        choices=[('de', 'Dễ'), ('trung binh', 'Trung bình'), ('kho', 'Khó')],
        required=False,
        allow_null=True,
        error_messages={
            'invalid_choice': 'cap_do phải là: "de", "trung binh", "kho" hoặc để trống.'
        }
    )    

    class Meta:
        model = HuongDan
        fields = ['id', 'tieu_de', 'thoi_gian_tao', 'noi_dung', 'nguoi_tao_id', 'cap_do']


class DatSanSerializer(serializers.ModelSerializer):
    san_id = serializers.PrimaryKeyRelatedField(queryset=San.objects.all())
    nguoi_dung_id = serializers.PrimaryKeyRelatedField(queryset=NguoiDung.objects.all())
    tong_tien = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = DatSan
        fields = ['id', 'thoi_gian_dat', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'san_id', 'nguoi_dung_id', 'so_luong_san', 'tong_tien']

    def validate(self, data):
        thoi_gian_bat_dau = data.get('thoi_gian_bat_dau')
        thoi_gian_ket_thuc = data.get('thoi_gian_ket_thuc')
        san = data.get('san_id')
        so_luong_san = data.get('so_luong_san')

        if thoi_gian_bat_dau and thoi_gian_ket_thuc:
            if thoi_gian_bat_dau >= thoi_gian_ket_thuc:
                raise serializers.ValidationError("Thời gian bắt đầu phải trước thời gian kết thúc.")
            if san:
                if thoi_gian_bat_dau < san.gio_mo_cua or thoi_gian_ket_thuc > san.gio_dong_cua:
                    raise serializers.ValidationError("Thời gian đặt phải nằm trong giờ mở cửa và đóng cửa của sân.")
                if so_luong_san and so_luong_san > san.so_san_con:
                    raise serializers.ValidationError("Số lượng sân đặt vượt quá số sân còn lại.")
        return data