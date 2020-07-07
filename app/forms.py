from django import forms
from .models import *

GENDER = [
    ('Nam', 'Nam'),
    ('Nữ', 'Nữ')
]
class DateInput(forms.DateInput):
    input_type='date'

class CreateStudent(forms.ModelForm):
    hoten = forms.CharField(label='Họ tên', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    ngaysinh = forms.DateField(widget=DateInput(attrs={
        'class': 'form-control'
    }), required=True)
    gender = forms.ChoiceField(choices=GENDER, label='Giới tính', widget=forms.Select(attrs={
        'class': 'form-control'
    }), required=True)
    nganh = forms.ModelChoiceField(queryset=Nganh.objects.all(), label='Ngành', widget=forms.Select(attrs={
        'class': 'form-control'
    }), required=True)
    hedt = forms.ModelChoiceField(queryset=HeDT.objects.all(), label='Hệ đào tạo', widget=forms.Select(attrs={
        'class': 'form-control'
    }), required=True)
    nien_khoa = forms.ModelChoiceField(queryset=NienKhoa.objects.all(), label='Niên khóa', widget=forms.Select(attrs={
        'class': 'form-control'
    }), required=True)
    class Meta:
        model = SinhVien
        fields = ('hoten', 'ngaysinh', 'gender', 'nganh', 'hedt', 'nien_khoa')

class HocKi_MonHoc(forms.ModelForm):
    class Meta:
        model = MonHoc
        fields = ('hocki',)


class CreateLop(forms.ModelForm):

    start_date = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}
    ))
    end_date = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}
    ))
    class Meta:
        model = Lop
        fields = '__all__'

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['ma_lop'].widget.attrs.update({'class': 'form-control'})
        self.fields['mon_hoc'].widget.attrs.update({'class': 'form-control'})
        self.fields['giang_vien'].widget.attrs.update({'class': 'form-control'})
        self.fields['thoi_gian_hoc'].widget.attrs.update({'class': 'form-control'})
        self.fields['si_so_max'].widget.attrs.update({'class': 'form-control'})
        self.fields['he_dt'].widget.attrs.update({'class': 'form-control'})
        self.fields['ghi_chu'].widget.attrs.update({'class': 'form-control'})



class CreateGiangVien(forms.ModelForm):
    ngaysinh = forms.DateField(widget=DateInput(
        attrs={'class': 'form-control'}
    ))
    class Meta:
        model = GiaoVien
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['ma_gv'].widget.attrs.update({'class': 'form-control'})
        self.fields['ho_ten'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['tot_nghiep_tai'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

class DangKiHoc(forms.ModelForm):
    class Meta:
        model = SinhVien
        fields = ('__all__')
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['lop'].widget.attrs.update({'class': 'form-control'})

class SelectHocKy(forms.ModelForm):
    class Meta:
        model = MonHoc
        fields = ('hocki',)
    # def __init__(self, *arg, **kwarg):
    #     super().__init__(*arg, **kwarg)
    #     self.fields['hocki'].widget.update({'maxlength': '50'})


class DongHocPhi(forms.ModelForm):
    class Meta:
        model = HocPhiDaDong
        fields = '__all__'
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['hoc_ki'].widget.attrs.update({'class': 'form-control'})
        self.fields['so_tien'].widget.attrs.update({'class': 'form-control'})

class HocPhiNo(forms.ModelForm):
    class Meta:
        model = HocPhiConNo
        fields = '__all__'


class FormHeDT(forms.ModelForm):
    class Meta:
        model = Lop
        fields = ('he_dt',)
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['he_dt'].widget.attrs.update({'class': 'form-control'})

class NganhForm(forms.ModelForm):
    class Meta:
        model = Nganh
        fields = ('khoa',)
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.fields['khoa'].widget.attrs.update({'class': 'form-control'})








