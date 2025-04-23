from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import SanChoi
import json
from django.core.exceptions import ValidationError

# Create your views here.

@require_http_methods(["GET"])
def get_all_courts(request):
    try:
        courts = SanChoi.objects.all()
        court_list = []
        for court in courts:
            court_list.append({
                'id': court.id,
                'ten_khu_vuc': court.ten_khu_vuc,
                'dia_diem': court.dia_diem,
                'gio_mo_cua': court.gio_mo_cua.strftime('%H:%M:%S'),
                'gio_dong_cua': court.gio_dong_cua.strftime('%H:%M:%S'),
                'gia_thue_theo_gio': str(court.gia_thue_theo_gio),
                'mo_ta': court.mo_ta,
                'so_san_con': court.so_san_con
            })
        return JsonResponse({'courts': court_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_court_details(request, court_id):
    try:
        court = SanChoi.objects.get(id=court_id)
        return JsonResponse({
            'id': court.id,
            'ten_khu_vuc': court.ten_khu_vuc,
            'dia_diem': court.dia_diem,
            'gio_mo_cua': court.gio_mo_cua.strftime('%H:%M:%S'),
            'gio_dong_cua': court.gio_dong_cua.strftime('%H:%M:%S'),
            'gia_thue_theo_gio': str(court.gia_thue_theo_gio),
            'mo_ta': court.mo_ta,
            'so_san_con': court.so_san_con
        })
    except SanChoi.DoesNotExist:
        return JsonResponse({'error': 'Sân chơi không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_court(request):
    try:
        data = json.loads(request.body)
        print("Received data:", data)  # Debug print
        
        # Validate required fields
        required_fields = ['ten_khu_vuc', 'dia_diem', 'gio_mo_cua', 'gio_dong_cua', 'gia_thue_theo_gio', 'so_san_con']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)
        
        # Convert time strings to time objects
        try:
            from datetime import datetime
            gio_mo_cua = datetime.strptime(data['gio_mo_cua'], '%H:%M:%S').time()
            gio_dong_cua = datetime.strptime(data['gio_dong_cua'], '%H:%M:%S').time()
        except ValueError as e:
            return JsonResponse({'error': f'Invalid time format: {str(e)}'}, status=400)
        
        # Convert price to Decimal
        try:
            from decimal import Decimal
            gia_thue_theo_gio = Decimal(data['gia_thue_theo_gio'])
        except (ValueError, TypeError) as e:
            return JsonResponse({'error': f'Invalid price format: {str(e)}'}, status=400)
        
        court = SanChoi(
            ten_khu_vuc=data['ten_khu_vuc'],
            dia_diem=data['dia_diem'],
            gio_mo_cua=gio_mo_cua,
            gio_dong_cua=gio_dong_cua,
            gia_thue_theo_gio=gia_thue_theo_gio,
            mo_ta=data.get('mo_ta', ''),
            so_san_con=data['so_san_con']
        )
        
        try:
            court.full_clean()  # This will trigger the clean() method and validators
            court.save()
            return JsonResponse({'message': 'Tạo sân chơi thành công', 'id': court.id}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e.message_dict) if hasattr(e, 'message_dict') else str(e)}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_court(request, court_id):
    try:
        court = SanChoi.objects.get(id=court_id)
        data = json.loads(request.body)
        
        # Update only provided fields
        if 'ten_khu_vuc' in data:
            court.ten_khu_vuc = data['ten_khu_vuc']
        if 'dia_diem' in data:
            court.dia_diem = data['dia_diem']
        if 'gio_mo_cua' in data:
            court.gio_mo_cua = data['gio_mo_cua']
        if 'gio_dong_cua' in data:
            court.gio_dong_cua = data['gio_dong_cua']
        if 'gia_thue_theo_gio' in data:
            court.gia_thue_theo_gio = data['gia_thue_theo_gio']
        if 'mo_ta' in data:
            court.mo_ta = data['mo_ta']
        if 'so_san_con' in data:
            court.so_san_con = data['so_san_con']
            
        court.full_clean()  # Validate the updated data
        court.save()
        return JsonResponse({'message': 'Cập nhật sân chơi thành công'})
    except SanChoi.DoesNotExist:
        return JsonResponse({'error': 'Sân chơi không tồn tại'}, status=404)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_court(request, court_id):
    try:
        court = SanChoi.objects.get(id=court_id)
        court.delete()
        return JsonResponse({'message': 'Xóa sân chơi thành công'})
    except SanChoi.DoesNotExist:
        return JsonResponse({'error': 'Sân chơi không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
