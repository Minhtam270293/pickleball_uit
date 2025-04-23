from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import DanhGiaSan
from django.contrib.auth.models import User
from courts.models import SanChoi
import json
from django.core.exceptions import ValidationError

# Create your views here.

@require_http_methods(["GET"])
def get_all_reviews(request):
    try:
        reviews = DanhGiaSan.objects.all()
        review_list = []
        for review in reviews:
            review_list.append({
                'id': review.id,
                'khu_vuc_san': {
                    'id': review.khu_vuc_san.id,
                    'ten_khu_vuc': review.khu_vuc_san.ten_khu_vuc
                },
                'nguoi_dung': {
                    'id': review.nguoi_dung.id,
                    'username': review.nguoi_dung.username
                },
                'diem_so': review.diem_so,
                'nhan_xet': review.nhan_xet,
                'ngay_danh_gia': review.ngay_danh_gia.strftime('%Y-%m-%d')
            })
        return JsonResponse({'reviews': review_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_review_details(request, review_id):
    try:
        review = DanhGiaSan.objects.get(id=review_id)
        return JsonResponse({
            'id': review.id,
            'khu_vuc_san': {
                'id': review.khu_vuc_san.id,
                'ten_khu_vuc': review.khu_vuc_san.ten_khu_vuc
            },
            'nguoi_dung': {
                'id': review.nguoi_dung.id,
                'username': review.nguoi_dung.username
            },
            'diem_so': review.diem_so,
            'nhan_xet': review.nhan_xet,
            'ngay_danh_gia': review.ngay_danh_gia.strftime('%Y-%m-%d')
        })
    except DanhGiaSan.DoesNotExist:
        return JsonResponse({'error': 'Đánh giá không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_review(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['khu_vuc_san_id', 'nguoi_dung_id', 'diem_so', 'nhan_xet']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)
        
        # Check if court and user exist
        try:
            court = SanChoi.objects.get(id=data['khu_vuc_san_id'])
            user = User.objects.get(id=data['nguoi_dung_id'])
        except SanChoi.DoesNotExist:
            return JsonResponse({'error': 'Khu vực sân không tồn tại'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Người dùng không tồn tại'}, status=404)
        
        # Check if user has already reviewed this court
        if DanhGiaSan.objects.filter(khu_vuc_san=court, nguoi_dung=user).exists():
            return JsonResponse({'error': 'Bạn đã đánh giá khu vực sân này rồi'}, status=400)
        
        review = DanhGiaSan(
            khu_vuc_san=court,
            nguoi_dung=user,
            diem_so=data['diem_so'],
            nhan_xet=data['nhan_xet']
        )
        
        try:
            review.full_clean()  # This will trigger the clean() method and validators
            review.save()
            return JsonResponse({'message': 'Tạo đánh giá thành công', 'id': review.id}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e.message_dict) if hasattr(e, 'message_dict') else str(e)}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_review(request, review_id):
    try:
        review = DanhGiaSan.objects.get(id=review_id)
        data = json.loads(request.body)
        
        # Update only provided fields
        if 'diem_so' in data:
            review.diem_so = data['diem_so']
        if 'nhan_xet' in data:
            review.nhan_xet = data['nhan_xet']
        
        try:
            review.full_clean()  # Validate the updated data
            review.save()
            return JsonResponse({'message': 'Cập nhật đánh giá thành công'})
        except ValidationError as e:
            return JsonResponse({'error': str(e.message_dict) if hasattr(e, 'message_dict') else str(e)}, status=400)
            
    except DanhGiaSan.DoesNotExist:
        return JsonResponse({'error': 'Đánh giá không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_review(request, review_id):
    try:
        review = DanhGiaSan.objects.get(id=review_id)
        review.delete()
        return JsonResponse({'message': 'Xóa đánh giá thành công'})
    except DanhGiaSan.DoesNotExist:
        return JsonResponse({'error': 'Đánh giá không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
