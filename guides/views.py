from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import HuongDanChoi
from django.contrib.auth.models import User
import json
from django.core.exceptions import ValidationError

# Create your views here.

@require_http_methods(["GET"])
def get_all_guides(request):
    try:
        guides = HuongDanChoi.objects.all()
        guide_list = []
        for guide in guides:
            guide_list.append({
                'id': guide.id,
                'tieu_de': guide.tieu_de,
                'nguoi_tao': {
                    'id': guide.nguoi_tao.id,
                    'username': guide.nguoi_tao.username
                },
                'thoi_gian_tao': guide.thoi_gian_tao.strftime('%Y-%m-%d %H:%M:%S'),
                'noi_dung': guide.noi_dung
            })
        return JsonResponse({'guides': guide_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_guide_details(request, guide_id):
    try:
        guide = HuongDanChoi.objects.get(id=guide_id)
        return JsonResponse({
            'id': guide.id,
            'tieu_de': guide.tieu_de,
            'nguoi_tao': {
                'id': guide.nguoi_tao.id,
                'username': guide.nguoi_tao.username
            },
            'thoi_gian_tao': guide.thoi_gian_tao.strftime('%Y-%m-%d %H:%M:%S'),
            'noi_dung': guide.noi_dung
        })
    except HuongDanChoi.DoesNotExist:
        return JsonResponse({'error': 'Hướng dẫn không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_guide(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['tieu_de', 'nguoi_tao_id', 'noi_dung']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)
        
        # Check if creator exists
        try:
            creator = User.objects.get(id=data['nguoi_tao_id'])
        except User.DoesNotExist:
            return JsonResponse({'error': 'Người tạo không tồn tại'}, status=404)
        
        guide = HuongDanChoi(
            tieu_de=data['tieu_de'],
            nguoi_tao=creator,
            noi_dung=data['noi_dung']
        )
        
        try:
            guide.full_clean()  # This will trigger the clean() method and validators
            guide.save()
            return JsonResponse({'message': 'Tạo hướng dẫn thành công', 'id': guide.id}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': str(e.message_dict) if hasattr(e, 'message_dict') else str(e)}, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_guide(request, guide_id):
    try:
        guide = HuongDanChoi.objects.get(id=guide_id)
        data = json.loads(request.body)
        
        # Update only provided fields
        if 'tieu_de' in data:
            guide.tieu_de = data['tieu_de']
        if 'noi_dung' in data:
            guide.noi_dung = data['noi_dung']
        
        try:
            guide.full_clean()  # Validate the updated data
            guide.save()
            return JsonResponse({'message': 'Cập nhật hướng dẫn thành công'})
        except ValidationError as e:
            return JsonResponse({'error': str(e.message_dict) if hasattr(e, 'message_dict') else str(e)}, status=400)
            
    except HuongDanChoi.DoesNotExist:
        return JsonResponse({'error': 'Hướng dẫn không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_guide(request, guide_id):
    try:
        guide = HuongDanChoi.objects.get(id=guide_id)
        guide.delete()
        return JsonResponse({'message': 'Xóa hướng dẫn thành công'})
    except HuongDanChoi.DoesNotExist:
        return JsonResponse({'error': 'Hướng dẫn không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
