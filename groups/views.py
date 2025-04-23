from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import NhomChoi, ThanhVienNhom
from django.contrib.auth.models import User
import json
from django.core.exceptions import ValidationError

@require_http_methods(["GET"])
def get_all_groups(request):
    try:
        groups = NhomChoi.objects.all()
        group_list = []
        for group in groups:
            group_list.append({
                'id': group.id,
                'ten_nhom': group.ten_nhom,
                'nguoi_tao': {
                    'id': group.nguoi_tao.id,
                    'username': group.nguoi_tao.username
                },
                'mo_ta': group.mo_ta,
                'thoi_gian_hoat_dong': group.thoi_gian_hoat_dong,
                'dia_diem_hoat_dong': group.dia_diem_hoat_dong
            })
        return JsonResponse({'groups': group_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_group_details(request, group_id):
    try:
        group = NhomChoi.objects.get(id=group_id)
        members = ThanhVienNhom.objects.filter(nhom=group)
        member_list = []
        for member in members:
            member_list.append({
                'id': member.thanh_vien.id,
                'username': member.thanh_vien.username,
                'ngay_tham_gia': member.ngay_tham_gia.strftime('%Y-%m-%d')
            })
        
        return JsonResponse({
            'id': group.id,
            'ten_nhom': group.ten_nhom,
            'nguoi_tao': {
                'id': group.nguoi_tao.id,
                'username': group.nguoi_tao.username
            },
            'mo_ta': group.mo_ta,
            'thoi_gian_hoat_dong': group.thoi_gian_hoat_dong,
            'dia_diem_hoat_dong': group.dia_diem_hoat_dong,
            'thanh_vien': member_list
        })
    except NhomChoi.DoesNotExist:
        return JsonResponse({'error': 'Nhóm không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_group(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['ten_nhom', 'nguoi_tao_id', 'mo_ta', 'thoi_gian_hoat_dong', 'dia_diem_hoat_dong']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)
        
        # Check if creator exists
        try:
            creator = User.objects.get(id=data['nguoi_tao_id'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'Người tạo không tồn tại'}, status=404)
        
        group = NhomChoi(
            ten_nhom=data['ten_nhom'],
            nguoi_tao=creator,
            mo_ta=data['mo_ta'],
            thoi_gian_hoat_dong=data['thoi_gian_hoat_dong'],
            dia_diem_hoat_dong=data['dia_diem_hoat_dong']
        )
        
        group.save()
        return JsonResponse({'message': 'Tạo nhóm thành công', 'id': group.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_group(request, group_id):
    try:
        group = NhomChoi.objects.get(id=group_id)
        data = json.loads(request.body)
        
        # Update only provided fields
        if 'ten_nhom' in data:
            group.ten_nhom = data['ten_nhom']
        if 'mo_ta' in data:
            group.mo_ta = data['mo_ta']
        if 'thoi_gian_hoat_dong' in data:
            group.thoi_gian_hoat_dong = data['thoi_gian_hoat_dong']
        if 'dia_diem_hoat_dong' in data:
            group.dia_diem_hoat_dong = data['dia_diem_hoat_dong']
        
        group.save()
        return JsonResponse({'message': 'Cập nhật nhóm thành công'})
    except NhomChoi.DoesNotExist:
        return JsonResponse({'error': 'Nhóm không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_group(request, group_id):
    try:
        group = NhomChoi.objects.get(id=group_id)
        group.delete()
        return JsonResponse({'message': 'Xóa nhóm thành công'})
    except NhomChoi.DoesNotExist:
        return JsonResponse({'error': 'Nhóm không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def add_member(request, group_id):
    try:
        data = json.loads(request.body)
        if 'user_id' not in data:
            return JsonResponse({'error': 'Missing user_id'}, status=400)
        
        group = NhomChoi.objects.get(id=group_id)
        user = User.objects.get(id=data['user_id'])
        
        # Check if user is already a member
        if ThanhVienNhom.objects.filter(nhom=group, thanh_vien=user).exists():
            return JsonResponse({'error': 'User is already a member of this group'}, status=400)
        
        ThanhVienNhom.objects.create(nhom=group, thanh_vien=user)
        return JsonResponse({'message': 'Thêm thành viên thành công'})
    except NhomChoi.DoesNotExist:
        return JsonResponse({'error': 'Nhóm không tồn tại'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def remove_member(request, group_id, user_id):
    try:
        group = NhomChoi.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        
        member = ThanhVienNhom.objects.get(nhom=group, thanh_vien=user)
        member.delete()
        return JsonResponse({'message': 'Xóa thành viên thành công'})
    except NhomChoi.DoesNotExist:
        return JsonResponse({'error': 'Nhóm không tồn tại'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User không tồn tại'}, status=404)
    except ThanhVienNhom.DoesNotExist:
        return JsonResponse({'error': 'User không phải là thành viên của nhóm'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
