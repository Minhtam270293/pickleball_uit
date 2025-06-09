from decimal import Decimal
from django.db.models import Sum
from pickleball_platform_management.models import DatSan, San

def tinh_tien_dat_san(dat_san_id):
    """
    Tính và cập nhật tổng tiền cho một lượt đặt sân (DatSan).
    Tổng tiền = giá thuê * số giờ * số lượng sân.
    Đồng thời cập nhật doanh thu của sân.
    """
    dat_san = DatSan.objects.select_related('san_id').get(id=dat_san_id)
    san = dat_san.san_id

    # Tính số giờ thuê
    bat_dau = dat_san.thoi_gian_bat_dau.hour * 60 + dat_san.thoi_gian_bat_dau.minute
    ket_thuc = dat_san.thoi_gian_ket_thuc.hour * 60 + dat_san.thoi_gian_ket_thuc.minute
    so_gio = Decimal(ket_thuc - bat_dau) / Decimal(60)
    if so_gio <= 0:
        tong_tien = Decimal(0)
    else:
        tong_tien = san.gia_thue_theo_gio * so_gio * dat_san.so_luong_san

    dat_san.tong_tien = tong_tien.quantize(Decimal('1.'))  # Làm tròn đến đơn vị
    dat_san.save(update_fields=['tong_tien'])

    return dat_san.tong_tien

def tinh_doanh_thu_san(san_id):
    san = San.objects.get(id=san_id)
    tong_tien = DatSan.objects.filter(san_id=san).aggregate(total=Sum('tong_tien'))['total'] or Decimal(0)
    san.doanh_thu = tong_tien
    san.save(update_fields=['doanh_thu'])
    return san.doanh_thu

def tinh_doanh_thu_tat_ca_san():
    for san in San.objects.all():
        tinh_doanh_thu_san(san.id)
    return list(San.objects.all())
