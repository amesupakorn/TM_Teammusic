from django.shortcuts import render, redirect
from django.views import View
from .models import *

class MainView(View):
    
    def get(self, request):
        return render(request, "index.html",{
            
        })
        
class Artlist(View):
    def get(self, request):
        return render(request, "artlist.html",{
            
        })
        
class Albums(View):
     def get(self, request):
        return render(request, "album.html",{
            
        })