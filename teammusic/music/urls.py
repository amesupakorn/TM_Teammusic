from django.urls import path
from . import views

urlpatterns = [
     path("", views.MainView.as_view(), name="home"),
     path("arttist", views.Artlist.as_view(), name="artist"),
     path("album", views.Albums.as_view(), name="albums"),
     
     path("signin", views.SignIn.as_view(), name="signin"),
     path("signup", views.SignUp.as_view(), name="signup")
     
]
