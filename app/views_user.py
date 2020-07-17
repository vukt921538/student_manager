from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .forms import *
from django.contrib import messages
from datetime import datetime, timedelta


# Create your views here.

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


def mon_hoc(request):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    form = HocKi_MonHoc()
    if request.method == 'POST':

        hk = request.POST.get('hocki')
        print(hk)

        t = HocKi.objects.get(id=hk)
        data = sv.lop.filter(mon_hoc__hocki=t, ghi_chu='LOPMOI')
    else:
        data = sv.lop.filter(ghi_chu='LOPMOI')

    total_tinchi = 0
    hk = request.POST.get('hocki')
    for i in data:
        print(i.giang_vien.ho_ten)
        total_tinchi += i.mon_hoc.tin_chi

    tkb_hoc_lai = sv.lop.filter(ghi_chu='HOCLAI')
    context = {
        'data': data,
        'total_tinchi': total_tinchi,
        'sv': sv,
        'form': form,
        'tkb_hoc_lai': tkb_hoc_lai
    }
    return render(request, 'mon_hoc.html', context)


def bang_diem(request):
    s = SinhVien.objects.get(user=request.user)
    data = s.lop.filter(ghi_chu='LOPMOI')
    for monhoc in data:
        monhoc.diem = Diem.objects.filter(
            mon_hoc__id=monhoc.mon_hoc.id, sinh_vien=s)
        for item in monhoc.diem:
            monhoc.diem.item_1 = item.diem_chuyen_can
            monhoc.diem.item_2 = item.diem_kiem_tra
            monhoc.diem.item_3 = item.diem_cuoi_ki
            try:
                temp = monhoc.diem.item_1 * 0.1 + \
                       monhoc.diem.item_2 * 0.2 + monhoc.diem.item_3 * 0.7
                monhoc.diem.tong_ket = round(temp, 2)

                if monhoc.diem.tong_ket < 4.0 or monhoc.diem.item_1 <= 2:
                    monhoc.diem.diem_chu = 'F'
                elif monhoc.diem.tong_ket >= 4.0 and monhoc.diem.tong_ket < 5:
                    monhoc.diem.diem_chu = 'D'
                elif monhoc.diem.tong_ket >= 5.0 and monhoc.diem.tong_ket < 5.5:
                    monhoc.diem.diem_chu = 'D+'
                elif monhoc.diem.tong_ket >= 5.5 and monhoc.diem.tong_ket < 6.5:
                    monhoc.diem.diem_chu = 'C'
                elif monhoc.diem.tong_ket >= 6.5 and monhoc.diem.tong_ket < 7:
                    monhoc.diem.diem_chu = 'C+'
                elif monhoc.diem.tong_ket >= 7.0 and monhoc.diem.tong_ket < 8:
                    monhoc.diem.diem_chu = 'B'
                elif monhoc.diem.tong_ket >= 8.0 and monhoc.diem.tong_ket < 8.5:
                    monhoc.diem.diem_chu = 'B+'
                elif monhoc.diem.tong_ket >= 8.5 and monhoc.diem.tong_ket <= 10:
                    monhoc.diem.diem_chu = 'A'

                if monhoc.diem.tong_ket < 4.0 or monhoc.diem.item_1 <= 2:
                    monhoc.diem.danh_gia = 'HOCLAI'
                elif monhoc.diem.tong_ket >= 4.0:
                    monhoc.diem.danh_gia = 'DAT'
            except:
                pass

    hocki_all = HocKi.objects.all()

    u = 0
    v = 0
    tong_tc_chua_dat = []  # của tất cả học kì nên phải để ngoauf for
    tong_diem = []
    tong_tin = []
    for i in hocki_all:
        i.ss = 6
        i.tong = 0
        i.tin_chi = 0
        i.diem = Diem.objects.filter(mon_hoc__hocki=i, sinh_vien=s)
        tc_chua_dat = []
        i.ttc = 0
        for d in i.diem:
            d.tc_chua_dat = 0
            i.diem.tong = 0
            i.diem.tin_chi = d.mon_hoc.tin_chi
            i.ttc += i.diem.tin_chi
            try:
                d.tong_ket = round(d.diem_chuyen_can * 0.1 +
                                   d.diem_kiem_tra * 0.2 + d.diem_cuoi_ki * 0.7, 2)
                if d.diem_chuyen_can <= 2:
                    d.tong_ket = 0
                elif d.tong_ket >= 8.5 and d.tong_ket <= 10:
                    d.tong_ket = 4
                elif d.tong_ket >= 8 and d.tong_ket < 8.5:
                    d.tong_ket = 3.5
                elif d.tong_ket >= 7 and d.tong_ket < 8:
                    d.tong_ket = 3
                elif d.tong_ket >= 6.5 and d.tong_ket < 7:
                    d.tong_ket = 2.5
                elif d.tong_ket >= 5.5 and d.tong_ket < 6.5:
                    d.tong_ket = 2
                elif d.tong_ket >= 5 and d.tong_ket < 5.5:
                    d.tong_ket = 1.5
                elif d.tong_ket >= 4 and d.tong_ket < 5:
                    d.tong_ket = 1
                elif d.tong_ket < 4:
                    d.tong_ket = 0
                i.tong += d.tong_ket
                print("TONG: ", i.tong)
                i.tin_chi += d.mon_hoc.tin_chi
                print("TIN_CHI: ", i.tin_chi)
                i.diem.tin = round(i.tong / i.tin_chi, 2)
                tong_diem.append(i.tong)
                tong_tin.append(i.tin_chi)
                if d.tong_ket == 0:
                    tc_chua_dat.append(d.mon_hoc.tin_chi)
            except:
                pass
        i.tc_false = sum(tc_chua_dat)
        tong_tc_chua_dat.append(i.tc_false)
    result_tc_chua_dat = sum(tong_tc_chua_dat)
    print(tong_diem)
    tin_chi_sum_all = sum(tong_tin)
    diem_he_4 = round(sum(tong_diem) / sum(tong_tin), 2)
    print(diem_he_4)
    form = SelectHocKy()
    if request.method == 'POST':
        form = SelectHocKy(request.POST)
        id_hocki = request.POST.get('hocki')
        print('ID: ', id_hocki)
        data = s.lop.filter(mon_hoc__hocki__id=id_hocki, ghi_chu='LOPMOI')
        for monhoc in data:
            monhoc.diem = Diem.objects.filter(
                mon_hoc__id=monhoc.mon_hoc.id, sinh_vien=s)
            for item in monhoc.diem:
                monhoc.diem.item_1 = item.diem_chuyen_can
                monhoc.diem.item_2 = item.diem_kiem_tra
                monhoc.diem.item_3 = item.diem_cuoi_ki
                try:
                    temp = monhoc.diem.item_1 * 0.1 + \
                           monhoc.diem.item_2 * 0.2 + monhoc.diem.item_3 * 0.7
                    monhoc.diem.tong_ket = round(temp, 2)

                    if monhoc.diem.tong_ket < 4.0 or monhoc.diem.item_1 <= 2:
                        monhoc.diem.diem_chu = 'F'
                    elif monhoc.diem.tong_ket >= 4.0 and monhoc.diem.tong_ket < 5:
                        monhoc.diem.diem_chu = 'D'
                    elif monhoc.diem.tong_ket >= 5.0 and monhoc.diem.tong_ket < 5.5:
                        monhoc.diem.diem_chu = 'D+'
                    elif monhoc.diem.tong_ket >= 5.5 and monhoc.diem.tong_ket < 6.5:
                        monhoc.diem.diem_chu = 'C'
                    elif monhoc.diem.tong_ket >= 6.5 and monhoc.diem.tong_ket < 7:
                        monhoc.diem.diem_chu = 'C+'
                    elif monhoc.diem.tong_ket >= 7.0 and monhoc.diem.tong_ket < 8:
                        monhoc.diem.diem_chu = 'B'
                    elif monhoc.diem.tong_ket >= 8.0 and monhoc.diem.tong_ket < 8.5:
                        monhoc.diem.diem_chu = 'B+'
                    elif monhoc.diem.tong_ket >= 8.5 and monhoc.diem.tong_ket <= 10:
                        monhoc.diem.diem_chu = 'A'

                    if monhoc.diem.tong_ket < 4.0 or monhoc.diem.item_1 <= 2:
                        monhoc.diem.danh_gia = 'HOCLAI'
                    elif monhoc.diem.tong_ket >= 4.0:
                        monhoc.diem.danh_gia = 'DAT'
                except:
                    pass

    context = {
        'data': data,
        'hocki_all': hocki_all,
        'tin_chi_all': v,
        'form': form,
        'tong_tin': tin_chi_sum_all,
        'tong_tc_chua_dat': result_tc_chua_dat,
        'sv': s,
        'diem_he_4': diem_he_4
    }
    sc = Diem.objects.filter(sinh_vien=s)
    return render(request, 'bang_diem.html', context)


def dang_ki_hoc(request):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    l = Lop.objects.all()

    # Lọc ra những lớp phải học lại thì đăng kí
    ds_lop_hoc_lai = []
    lop_hoc_lai = Lop.objects.filter(ghi_chu='HOCLAI')
    for lop in lop_hoc_lai:
        if sv.lop.filter(mon_hoc=lop.mon_hoc).exists():
            d = Diem.objects.filter(sinh_vien=sv, mon_hoc=lop.mon_hoc)
            print('DDĐ: ', d)
            for i in d:
                try:
                    tk = round(i.diem_chuyen_can * 0.1 +
                               i.diem_kiem_tra * 0.2 + i.diem_cuoi_ki * 0.7, 2)
                    if i.diem_chuyen_can <= 2 or tk < 4:
                        lop.ds_lop = lop
                    if lop.ds_lop.deadline >= datetime.now():
                        lop.check = True
                        print("OK: ", lop.ds_lop)
                    ds_lop_hoc_lai.append(lop.ds_lop)
                except:
                    pass
    for i in ds_lop_hoc_lai:
        i.count = SinhVien.objects.filter(lop=i).count()

    # Đăng kí lớp
    ds_moi = sv.lop.filter(ghi_chu='HOCLAI')
    now = datetime.now()
    for item in ds_moi:
        if now >= item.deadline:
            item.out_of_date = True
        item.disable_button = False
        don_gia = item.mon_hoc.tin_chi * 300000
        item.count_sv = SinhVien.objects.filter(lop=item).count()
        item.temp = DangKiHocThanhCong.objects.get(lop__id=item.id)
        time_data = item.temp.time
        item.s = time_data.strftime('%m/%d/%Y %H:%M:%S')
        durations = timedelta(days=1)
        end_time = time_data + durations
        if now >= end_time:
            item.disable_button = True

    if len(ds_moi) != 0:
        context = {
            'sv': sv,
            'l': l,
            'ds_lop_hoc_lai': ds_lop_hoc_lai,
            'ds_moi': ds_moi,
            'disable_button': item.disable_button
        }
    else:
        context = {
            'sv': sv,
            'l': l,
            'ds_lop_hoc_lai': ds_lop_hoc_lai,
            'ds_moi': ds_moi,
        }
    return render(request, 'dang_ki_hoc.html', context)


def huy_lop_hoc_lai(request, id):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    l = Lop.objects.get(pk=id)
    w = Diem.objects.filter(mon_hoc=l.mon_hoc, sinh_vien=sv)
    sv.lop.remove(l)
    h = HocPhiConNo.objects.get(user=user, hoc_ki=l.mon_hoc.hocki)
    h.so_tien_con_no -= l.mon_hoc.tin_chi * 300000
    h.save()
    messages.add_message(request, messages.SUCCESS, "Thao tác thành công!")
    return redirect('dang_ki_hoc')


def huy_lop(request, id):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    l = Lop.objects.get(pk=id)
    w = Diem.objects.filter(mon_hoc=l.mon_hoc, sinh_vien=sv)
    sv.lop.remove(l)
    h = HocPhiConNo.objects.get(user=user, hoc_ki=l.mon_hoc.hocki)
    h.so_tien_con_no -= l.mon_hoc.tin_chi * 300000
    h.save()
    messages.add_message(request, messages.SUCCESS, "Thao tác thành công!")
    return redirect('dang_ki_hoc_chinh')


def dang_ki_lop(request, id):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    t = 300000
    a = Lop.objects.get(pk=id)
    if sv.lop.filter(ghi_chu='HOCLAI', mon_hoc=a.mon_hoc).exists():
        messages.add_message(request, messages.ERROR,
                             "Bạn đã đăng kí học phần này!")
    else:
        if sv.lop.filter(ghi_chu='HOCLAI', thoi_gian_hoc=a.thoi_gian_hoc):
            messages.add_message(request, messages.ERROR,
                                 "Bị trùng lịch học, vui lòng kiểm tra lại!")
        elif SinhVien.objects.filter(lop=a).count() < a.si_so_max:
            sv.lop.add(a)
            if DangKiHocThanhCong.objects.filter(lop=a).exists():
                s = DangKiHocThanhCong.objects.get(lop=a)
                s.save()
            else:
                DangKiHocThanhCong.objects.create(
                    lop=a,
                )
            try:
                k = DangKiHocThanhCong.objects.get(lop__id=a.id)
                s = HocPhiConNo.objects.get(user=user, hoc_ki=a.mon_hoc.hocki)
                s.so_tien_con_no += a.mon_hoc.tin_chi * t
                s.save()
            except:
                z = a.mon_hoc.tin_chi * t
                HocPhiConNo.objects.create(
                    user=user,
                    hoc_ki=a.mon_hoc.hocki,
                    so_tien_con_no=z
                )
            # Đăng kí lớp thành công thì cập nhật bảng HocPhi

            messages.add_message(request, messages.SUCCESS,
                                 "Đăng kí thành công!")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Không thể đăng kí lớp này (MAX_MEMBERS) !")
    return redirect('dang_ki_hoc')


def tra_hoc_phi(request):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    a = sv.lop.all()
    # Tổng số tín chỉ
    tin_chi = []
    for t in a:
        tin_chi.append(t.mon_hoc.tin_chi)

    hocphi_con = HocPhiConNo.objects.filter(user=user)
    hocphi_dong = HocPhiDaDong.objects.filter(user=user)
    tong_tien_no = []
    tong_tien_du = []
    for j in hocphi_con:
        j.t = 0
        for i in sv.lop.all():
            if j.hoc_ki == i.mon_hoc.hocki:
                j.t += i.mon_hoc.tin_chi
        if j.so_tien_con_no <= 0:
            j.so_du += j.so_tien_con_no * -1
            j.so_tien_con_no = 0

        tong_tien_du.append(j.so_du)
        tong_tien_no.append(j.so_tien_con_no)
    if sum(tong_tien_no) >= sum(tong_tien_du):
        result = sum(tong_tien_no) - sum(tong_tien_du)
    else:
        result = 0

    tong_dong = []
    for i in hocphi_dong:
        tong_dong.append(i.so_tien)

    tong = sum(tin_chi)
    data = sv.lop.all()
    hk = HocKi.objects.all()
    tong_all = 0
    for i in hk:
        i.tong_tc = 0
        i.tong_t = 0
        for d in data:
            if d.mon_hoc.hocki == i:
                i.tong_tc += d.mon_hoc.tin_chi
                i.tong_t += d.mon_hoc.tin_chi * 300000
        tong_all += i.tong_t

    context = {
        'sv': sv,
        'tong': tong,
        'result': result,
        'hocphi_con': hocphi_con,
        'hocphi_dong': hocphi_dong,
        'hk': hk,
        'tong_all': tong_all,
        'du': sum(tong_tien_du),
        'tong_dong': sum(tong_dong)
    }
    return render(request, 'tra_hoc_phi.html', context)


def hoc_chinh(request):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)
    l = Lop.objects.filter(mon_hoc__nganh=sv.nganh, ghi_chu='LOPMOI')
    hidden = False
    out_of_date = False
    now = datetime.now()
    for i in l:
        i.count = SinhVien.objects.filter(lop=i).count()
        if now >= i.deadline:
            i.out_of_date = True
        if i.count >= i.si_so_max:
            i.hidden = True
    data = sv.lop.filter(ghi_chu='LOPMOI')
    for i in data:
        i.disable_button = False
        i.new_lop = DangKiHocThanhCong.objects.get(lop__id=i.id).time
        i.fmt_time = i.new_lop.strftime('%d/%m/%Y-%H:%M:%S')
        i.si_so = SinhVien.objects.filter(lop=i).count()
        durations = timedelta(days=1)
        end_date = i.new_lop + durations
        if now >= end_date:
            i.disable_button = True

    if len(data) == 0:
        context = {
            'sv': sv,
            'lop': l,
            'data': data,
        }
    else:
        context = {
            'sv': sv,
            'lop': l,
            'data': data,
            'disable_button': i.disable_button
        }
    return render(request, 'hoc_chinh.html', context)


def dang_ki_chinh(request, id):
    user = User.objects.get(username=request.user)
    sv = SinhVien.objects.get(user=user)

    l = Lop.objects.get(pk=id)
    if sv.lop.filter(mon_hoc=l.mon_hoc).exists():
        messages.add_message(request, messages.ERROR,
                             'Bạn đã đăng kí học phần này!')
    elif sv.lop.filter(thoi_gian_hoc=l.thoi_gian_hoc).exists():
        messages.add_message(request, messages.ERROR,
                             'Bị trùng lịch, vui lòng kiểm tra lại!')
    else:
        data = Lop.objects.filter(mon_hoc__nganh=sv.nganh, ghi_chu='LOPMOI')
        sv.lop.add(l)
        sv.save()
        try:
            new_lop = DangKiHocThanhCong.objects.get(lop__id=l.id)
            new_lop.save()

        except:
            DangKiHocThanhCong.objects.create(
                lop=l,
            )
        try:
            a = HocPhiConNo.objects.get(user=user, hoc_ki=l.mon_hoc.hocki)
            a.so_tien_con_no += l.mon_hoc.tin_chi * 300000
            a.save()

        except:
            HocPhiConNo.objects.create(
                user=user,
                hoc_ki=l.mon_hoc.hocki,
                so_tien_con_no=l.mon_hoc.tin_chi * 300000
            )
        messages.add_message(request, messages.SUCCESS, 'Đăng kí thành công!')
    return redirect('dang_ki_hoc_chinh')


def inbox(request):
    u = User.objects.get(username=request.user)
    s = SinhVien.objects.get(user=u)
    inbox_list = Messages.objects.filter(receiver=s)
    return render(request, 'inbox.html', context={
        'inbox': inbox_list
    })


def detail_messages(request, id):
    mess_id = Messages.objects.get(pk=id)
    mess_id.seen = True
    mess_id.save()
    return render(request, 'detail_messages.html', context={
        'mess_id': mess_id
    })


def delete_inbox(request, id):
    mess_id = Messages.objects.get(pk=id)
    mess_id.delete()
    return redirect('inbox')
