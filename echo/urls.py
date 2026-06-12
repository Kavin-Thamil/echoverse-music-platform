from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_song, name='upload'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('song/<int:song_id>/delete/', views.delete_song, name='delete_song'),
    path('my-uploads/', views.my_uploads, name='my_uploads'),
    path('song/<int:song_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
]