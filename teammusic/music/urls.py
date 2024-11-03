from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("", views.MainView.as_view(), name="home"),
     path("arttist/<int:id>/", views.Artlist.as_view(), name="artist"),
     path("album/<int:id>/", views.Albums.as_view(), name="albums"),
     
     path("signin", views.SignIn.as_view(), name="signin"),
     path("signup/", views.SignUp.as_view(), name="signup"),
     path("confirm/", views.ConfirmEmail.as_view(), name="confirmemail"),
     path('logout/', views.LogoutView.as_view(), name='logout'),
     
     path('set_song_session/', views.set_song_session, name='set_song_session'),
     path('get_song_session/', views.get_song_session, name='get_song_session'),

     path('viewlist/<int:id>/', views.PlayListView.as_view(), name="viewPlaylist"),
     path('create_playlist/', views.CreatePlayList.as_view(), name='create_playlist'),

    path('playlist/<int:playlist_id>/add_song/<int:song_id>/', views.add_song_to_playlist, name='add_song_to_playlist'),


]

if settings.DEBUG:  # ใช้เฉพาะในโหมด DEBUG
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
