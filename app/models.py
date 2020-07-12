from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Khoa(models.Model):
    tenkhoa = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.tenkhoa


class Nganh(models.Model):
    tennganh = models.CharField(max_length=30, unique=True)
    khoa = models.ForeignKey(Khoa, on_delete=models.CASCADE)
    key_nganh = models.CharField(max_length=10, null=True, blank=True, unique=True)

    def __str__(self):
        return f'{self.tennganh} ({self.key_nganh}) ({self.khoa.tenkhoa})'


class HeDT(models.Model):
    tenhe = models.CharField(max_length=10)
    key = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.tenhe} ({self.key})'


class NienKhoa(models.Model):
    ten_nienkhoa = models.CharField(max_length=20)
    namhoc = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.ten_nienkhoa} ({self.namhoc})'


class HocKi(models.Model):
    ten_hk = models.IntegerField()

    def __str__(self):
        return f'{self.ten_hk}'


class MonHoc(models.Model):
    hocki = models.ForeignKey(HocKi, verbose_name='Chọn học kỳ ', on_delete=models.CASCADE)
    nganh = models.ForeignKey(Nganh, on_delete=models.CASCADE)
    ma_mon = models.CharField(max_length=10, unique=True)
    tenmon = models.CharField(max_length=30)
    tin_chi = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.tenmon} ({self.nganh})'


class GiaoVien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ma_gv = models.CharField(verbose_name="Mã giáo viên", max_length=10, unique=True)
    ho_ten = models.CharField(verbose_name="Họ tên", max_length=30)
    ngaysinh = models.CharField(verbose_name="Ngày sinh", max_length=20)
    address = models.CharField(verbose_name="Địa chỉ", max_length=50, null=True, blank=True)
    tot_nghiep_tai = models.CharField(verbose_name="Tốt nghiệp tại", max_length=30, null=True, blank=True)
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return f'{self.ma_gv} ({self.ho_ten})'


class ThoiGianHoc(models.Model):
    thu = models.CharField(max_length=10)
    tiet = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.thu}-{self.tiet}'


class Lop(models.Model):
    GHI_CHU = (
        ('HOCLAI', 'Học lại'),
        ('LOPMOI', 'Lớp mới')
    )
    ma_lop = models.CharField(verbose_name='Mã lớp', max_length=10, unique=True)
    mon_hoc = models.ForeignKey(MonHoc, verbose_name='Môn học', on_delete=models.CASCADE)
    giang_vien = models.ForeignKey(GiaoVien, verbose_name='Giảng viên', on_delete=models.CASCADE)
    thoi_gian_hoc = models.ForeignKey(ThoiGianHoc, verbose_name='Thời gian học', on_delete=models.CASCADE, null=True,
                                      blank=True)
    si_so_max = models.IntegerField(verbose_name='Sĩ số tối đa')
    created = models.DateTimeField(auto_now=True)
    start_date = models.DateField(verbose_name='Ngày bắt đầu')
    end_date = models.DateField(verbose_name='Ngày kết thúc')
    he_dt = models.ForeignKey(HeDT, verbose_name='Hệ đào tạo', on_delete=models.CASCADE)
    ghi_chu = models.CharField(
        verbose_name='Ghi chú',
        choices=GHI_CHU,
        max_length=20,
    )
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.mon_hoc.tenmon} ({self.giang_vien.ho_ten})' if self.mon_hoc else 'UN'


class SinhVien(models.Model):
    GENDER = [
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    hoten = models.CharField(verbose_name='Họ tên', max_length=30)
    ngaysinh = models.CharField(verbose_name='Ngày sinh', max_length=30)
    gender = models.CharField(
        choices=GENDER,
        verbose_name='Giới tính',
        max_length=10,
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    hocluc = models.CharField(max_length=10, blank=True)
    lop = models.ManyToManyField(Lop, blank=True)
    nganh = models.ForeignKey(Nganh, verbose_name='Ngành', on_delete=models.CASCADE, null=True, blank=True)
    hedt = models.ForeignKey(HeDT, verbose_name='Hệ đào tạo', on_delete=models.CASCADE, blank=True, null=True)
    nien_khoa = models.ForeignKey(NienKhoa, verbose_name='Niên khóa', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'{self.hoten} ({self.user.username})' if self.user else 'None'


class Diem(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    diem_chuyen_can = models.FloatField(null=True, blank=True)
    diem_kiem_tra = models.FloatField(null=True, blank=True)
    diem_cuoi_ki = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.mon_hoc.tenmon


class DiemHocLai(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    diem_chuyen_can = models.FloatField(null=True, blank=True)
    diem_kiem_tra = models.FloatField(null=True, blank=True)
    diem_cuoi_ki = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.mon_hoc.tenmon


class HocPhiDaDong(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    hoc_ki = models.ForeignKey(HocKi, verbose_name='Chọn học kì', on_delete=models.CASCADE)
    so_tien = models.IntegerField(verbose_name='Nhập số tiền cần đóng')

    def __str__(self):
        return self.user.username


class HocPhiConNo(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    hoc_ki = models.ForeignKey(HocKi, verbose_name='Chọn học kì', on_delete=models.CASCADE)
    so_tien_con_no = models.IntegerField(verbose_name='Số tiền')
    so_du = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actions = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)


class DangKiHocThanhCong(models.Model):
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)


class Messages(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE, null=True, blank=True)
    messages = models.TextField(null=True, blank=True)
    receiver = models.ForeignKey(SinhVien, related_name='receive', on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now=True)


# Xóa sinh viên sẽ xóa luôn dữ liệu có sẵn của User
@receiver(post_delete, sender=SinhVien)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()


# Xóa giảng viên sẽ xóa luôn dữ liệu có sẵn của User
@receiver(post_delete, sender=GiaoVien)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:
        instance.user.delete()
