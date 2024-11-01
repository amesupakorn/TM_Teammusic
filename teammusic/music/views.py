from django.shortcuts import render, redirect
from django.views import View
from .models import *
import boto3
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse


cognito_client = boto3.client('cognito-idp', region_name=settings.COGNITO_REGION)


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


class SignIn(View):
    def get(self, request):
        
        return render(request, "account/signin.html",{
            
        })
    def post(self, request):
        # รับข้อมูลจากฟอร์ม
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            # ใช้ Cognito เพื่อ Authenticate ผู้ใช้
            response = cognito_client.initiate_auth(
                ClientId=settings.COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                }
            )

            id_token = response['AuthenticationResult']['IdToken']
            access_token = response['AuthenticationResult']['AccessToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']
            
            # คุณสามารถจัดเก็บโทเค็นเหล่านี้ใน session หรือ cookie ได้
            # request.session['id_token'] = id_token
            # request.session['access_token'] = access_token
            # request.session['refresh_token'] = refresh_token

            messages.success(request, 'Login successful')
            return redirect('home') 
        
        except cognito_client.exceptions.NotAuthorizedException:
            messages.error(request, 'Invalid username or password')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

        return render(request, "account/signin.html")
   
        

class SignUp(View):
    def get(self, request):
        return render(request, "account/signup.html",{
            
        })
    def post(self, request):
            # รับข้อมูลจากฟอร์ม
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            try:
                # เรียกใช้ Cognito เพื่อสร้างผู้ใช้ใหม่
                response = cognito_client.sign_up(
                    ClientId=settings.COGNITO_CLIENT_ID,
                    Username=username,
                    Password=password,
                    UserAttributes=[
                        {'Name': 'email', 'Value': email},
                    ]
                )
                messages.success(request, 'Please confirm your email to complete registration.')
                return redirect('login')
            
            except cognito_client.exceptions.UsernameExistsException:
                messages.error(request, 'Username already exists')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
            
            return render(request, "account/signup.html")