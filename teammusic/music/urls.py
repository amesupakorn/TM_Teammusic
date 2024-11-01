from django.urls import path
from . import views

urlpatterns = [
     path("", views.MainView.as_view(), name="index"),
     path("arttist", views.Artlist.as_view(), name="artist"),
     path("album", views.Albums.as_view(), name="albums")
     
]
