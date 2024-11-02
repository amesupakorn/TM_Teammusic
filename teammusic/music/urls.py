from django.urls import path
from . import views

urlpatterns = [
     path("", views.MainView.as_view(), name="home"),
     path("arttist/<int:id>/", views.Artlist.as_view(), name="artist"),
     path("album/<int:id>/", views.Albums.as_view(), name="albums"),
     
     path("signin", views.SignIn.as_view(), name="signin"),
     path("signup/", views.SignUp.as_view(), name="signup"),
     path("confirm/", views.ConfirmEmail.as_view(), name="confirmemail"),
     path('logout/', views.LogoutView.as_view(), name='logout'),
     
     path('set_song_session/', views.set_song_session, name='set_song_session'),

]
