from django.urls import path
from . import views_user as user_views, views_staff as staff_views, views_admin as admin_views, views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_student/', admin_views.create, name='create_student'),
    path('upload_avata/', views.upload_avata, name='upload_avata'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('mon_hoc/', user_views.mon_hoc, name='mon_hoc'),
    path('bang_diem/', user_views.bang_diem, name='bang_diem'),
    path('lop_giang_day/', staff_views.lop_giang_day, name='lop_giang_day'),
    path('nhap_diem/<int:id>', staff_views.nhap_diem, name='nhap_diem'),
    path('insert_data/', staff_views.insert_data, name='insert_data'),
    path('read_excel/', staff_views.export_csv, name='export_csv'),
    path('import_csv/', admin_views.import_csv, name='import_csv'),
    path('list_student_lop/<int:id>/', admin_views.list_student_lop, name='list_student_lop'),
    path('detail_student/<int:id>/', admin_views.detail_student, name='detail_student'),
    path('delete_student/<int:id>/', admin_views.delete_student, name='delete_student'),
    path('add_menu', admin_views.menu_add, name='add_menu'),
    path('search/', admin_views.search, name='search'),
    path('list_student/', admin_views.list_student, name='list_student'),
    path('list_teacher/', admin_views.list_teacher, name='list_teacher'),
    path('delete_user/<int:id>', admin_views.delete_user, name='delete_user'),
    path('create_class/', admin_views.create_lop, name='create_lop'),
    path('create_teacher/', admin_views.create_teacher, name='create_teacher'),
    path('delete_teacher/<int:id>', admin_views.delete_teacher, name='delete_teacher'),
    path('detail_teacher/<int:id>', admin_views.detail_teacher, name='detail_teacher'),
    path('delete_lop/<int:id>', admin_views.delete_lop, name='delete_lop'),
    path('lop/', admin_views.lop, name='lop'),
    path('dang_ki_hoc', user_views.dang_ki_hoc, name='dang_ki_hoc'),
    path('huy_lop/<int:id>', user_views.huy_lop, name='huy_lop'),
    path('dang_ki_lop/<int:id>', user_views.dang_ki_lop, name='dang_ki_lop'),
    path('hoc_phi', admin_views.hoc_phi, name='hoc_phi'),
    path('tra_hoc_phi', user_views.tra_hoc_phi, name='tra_hoc_phi'),
    path('dong_hoc_phi', admin_views.dong_hoc_phi, name='dong_hoc_phi'),
    path('dang_ki_hoc_chinh', user_views.hoc_chinh, name='dang_ki_hoc_chinh'),
    path('dang_ki_chinh/<int:id>', user_views.dang_ki_chinh, name='dang_ki_chinh'),
    path('huy_lop_hoc_lai/<int:id>', user_views.huy_lop_hoc_lai, name='huy_lop_hoc_lai'),
    path('nhap_diem_excel/', staff_views.nhap_diem_excel, name='nhap_diem_excel'),
    path('delete_gd/<int:id>/', admin_views.delete_gd, name='delete_gd'),
    path('history/', admin_views.history, name='history'),
    path('send_messages', admin_views.send_messages, name='send_messages'),
    path('filter_student', admin_views.filter_student, name='filter_student'),
    path('inbox', user_views.inbox, name='inbox'),
    path('detail_messages/<int:id>/', user_views.detail_messages, name='detail_messages'),
    path('delete_inbox/<int:id>/', user_views.delete_inbox, name='delete_inbox')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
