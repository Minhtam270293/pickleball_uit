from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import NguoiDung

import json

# Create your views here.

# @require_http_methods(["GET"])
# def get_all_users(request):
#     try:
#         users = User.objects.all()
#         user_list = []
#         for user in users:
#             try:
#                 profile = NguoiDung.objects.get(user=user)
#                 user_list.append({
#                     'id': user.id,
#                     'username': user.username,
#                     'email': user.email,
#                     'ho_ten': profile.ho_ten,
#                     'so_dien_thoai': profile.so_dien_thoai,
#                     'dia_chi': profile.dia_chi,
#                     'loai_nguoi_dung': profile.loai_nguoi_dung
#                 })
#             except NguoiDung.DoesNotExist:
#                 continue
#         return JsonResponse({'users': user_list})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        ho_ten = data.get('ho_ten')
        
        # Required fields
        if not all([username, password, ho_ten]):
            return JsonResponse({'error': 'Thiếu thông tin bắt buộc (username, password, ho_ten)'}, status=400)

        # Optional fields
        email = data.get('email', '')
        so_dien_thoai = data.get('so_dien_thoai', '')
        dia_chi = data.get('dia_chi', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Tên đăng nhập đã tồn tại'}, status=400)

        # create_user automatically hashes the password
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        NguoiDung.objects.create(
            user=user,
            ho_ten=ho_ten,
            so_dien_thoai=so_dien_thoai,
            dia_chi=dia_chi
        )

        return JsonResponse({'message': 'Đăng ký thành công'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Đăng nhập thành công',
                'user_id': user.id,
                'username': user.username
            })
        return JsonResponse({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# @require_http_methods(["GET"])
# def user_profile(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         profile = NguoiDung.objects.get(user=user)
#         return JsonResponse({
#             'username': user.username,
#             'email': user.email,
#             'ho_ten': profile.ho_ten,
#             'so_dien_thoai': profile.so_dien_thoai,
#             'dia_chi': profile.dia_chi,
#             'loai_nguoi_dung': profile.loai_nguoi_dung
#         })
#     except User.DoesNotExist:
#         return JsonResponse({'error': 'Người dùng không tồn tại'}, status=404)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = NguoiDung.objects.get(user=user)
        data = json.loads(request.body)

        # Update User model fields
        if 'email' in data:
            user.email = data['email']
        if 'username' in data:
            if User.objects.filter(username=data['username']).exclude(id=user_id).exists():
                return JsonResponse({'error': 'Tên đăng nhập đã tồn tại'}, status=400)
            user.username = data['username']
        if 'password' in data:
            user.set_password(data['password'])
        user.save()

        # Update NguoiDung model fields
        if 'ho_ten' in data:
            profile.ho_ten = data['ho_ten']
        if 'so_dien_thoai' in data:
            profile.so_dien_thoai = data['so_dien_thoai']
        if 'dia_chi' in data:
            profile.dia_chi = data['dia_chi']
        if 'loai_nguoi_dung' in data:
            profile.loai_nguoi_dung = data['loai_nguoi_dung']
        profile.save()

        return JsonResponse({'message': 'Cập nhật thông tin thành công'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Người dùng không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'Xóa người dùng thành công'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Người dùng không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def user_logout(request):
    logout(request)
    return JsonResponse({'message': 'Đăng xuất thành công'})
