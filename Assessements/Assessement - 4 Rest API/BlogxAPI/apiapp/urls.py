from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('profile/', views.user_profile, name='user_profile'),
    path('posts/', views.post_list_create, name='post_list_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/comments/', views.comments_view, name='comments_view'),
]
