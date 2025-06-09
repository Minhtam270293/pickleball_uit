from rest_framework.routers import DefaultRouter
from .views import NguoiDungViewSet, SanViewSet, DanhGiaSanViewSet, HuongDanViewSet, DatSanViewSet

router = DefaultRouter()
router.register(r'users', NguoiDungViewSet, basename='nguoidung')
router.register(r'courts', SanViewSet, basename='san')
router.register(r'reviews', DanhGiaSanViewSet, basename='danhgiasan')
router.register(r'guides', HuongDanViewSet, basename='huongdan')
router.register(r'bookings', DatSanViewSet, basename='datsan')

urlpatterns = router.urls

