from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .forms import *
import random
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook


def index(request):
    if request.user.is_superuser:
        return redirect('home')
    # sv = SinhVien.objects.get(user=request.user)
    if request.user.is_anonymous:
        return redirect('login')
    get_user = User.objects.get(username=request.user)
    print(get_user)
    if request.user.is_superuser:
        user_login = SinhVien.objects.get(user=get_user)
    elif request.user.is_staff :
        user_login = GiaoVien.objects.get(user=get_user)
    else:
        user_login = SinhVien.objects.get(user=get_user)
    
    if not request.user.is_staff:
        messages = Messages.objects.filter(receiver=user_login)
        is_new_message = False
        count_new_messages = 0
        for message in messages:
            print(message.seen)
            if message.seen == False:
                count_new_messages += 1
                is_new_message = True
    else:
        count_new_messages = 0
        is_new_message = False
    context = {
        'user_login': user_login,
        'count_new_messages': count_new_messages,
        'is_new_message': is_new_message
    }
    return render(request, 'index.html', context)

def login(request):
    error_login = ''
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('pass')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            error_login = 'Đăng nhập thất bại'
    context = {
        'error_login': error_login
    }
    return render(request, 'login.html', context)

def upload_avata(request):
    if request.method == 'POST':
        files = request.FILES.get('avata', None)
        print('FILEEEE: ', files)

        # Lưu tên avata của sinh viên theo mã sinh viên
        filename = request.user.username + '.png'
        fs = FileSystemStorage()

        # Nếu ảnh đã có sẵn thì xoá đi rồi thêm mới
        if fs.exists(filename):
            fs.delete(filename)
        out_put = fs.save(filename, files)
        messages.add_message(request, messages.SUCCESS, 'Cập nhật ảnh đại diện thành công !')
    return redirect('/')

def edit_profile(request):
    # Get data from FORM:
    full_name = request.POST.get('fullname')
    ngaysinh = request.POST.get('ngaysinh')
    address = request.POST.get('address')
    email = request.POST.get('email')
    gender = request.POST.get('gender')
    phone = request.POST.get('phone')
    print('GEN: ', gender)
    print('gender: ', type(gender))
    # GET request.user
    user = User.objects.get(username=request.user)

    # UPDATE profile
    if request.user.is_staff:
        update_profile = GiaoVien.objects.get(user=user)
    else:
        update_profile = SinhVien.objects.get(user=user)
    
    if request.user.is_staff:
        update_profile.ho_ten = full_name

    update_profile.hoten = full_name
    try:
        update_profile.ngaysinh = ngaysinh
        update_profile.email = email
        update_profile.gender = gender
        update_profile.address = address
        update_profile.save()
        messages.add_message(request, messages.SUCCESS, 'Cập nhật thông tin thành công!')
    except:
        messages.add_message(request, messages.ERROR, 'Cập nhật thất bại!')
    print(type(user))
    print('Done')
    return redirect('/')
