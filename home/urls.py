from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('like_post/<int:id>/',  views.like_post, name='like_post'),
    path('dislike_post/<int:id>/',  views.dislike_post, name='dislike_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('reply_comment/<int:id>/', views.reply_comment, name='reply_comment'),
    path('search/', views.search_post, name='search_post')
]