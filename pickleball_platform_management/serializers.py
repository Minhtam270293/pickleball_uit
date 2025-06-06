from rest_framework import serializers
from .models import NguoiDung, San, DanhGiaSan, HuongDan

class NguoiDungSerializer(serializers.ModelSerializer):
    class Meta:
        model = NguoiDung
        exclude = ['vai_tro']

class SanSerializer(serializers.ModelSerializer):
    class Meta:
        model = San
        fields = '__all__'

    def validate(self, data):
        gio_mo_cua = data.get('gio_mo_cua')
        gio_dong_cua = data.get('gio_dong_cua')
        if gio_mo_cua and gio_dong_cua and gio_mo_cua >= gio_dong_cua:
            raise serializers.ValidationError("Giờ mở cửa phải trước giờ đóng cửa.")
        return data

class DanhGiaSanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhGiaSan
        fields = '__all__'

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
