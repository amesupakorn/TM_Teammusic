from django.shortcuts import render, redirect
from django.views import View
from .models import *
import boto3
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import jwt

cognito_client = boto3.client('cognito-idp', region_name=settings.COGNITO_REGION)


def get_username_from_access_token(access_token):
    try:
        # ถอดรหัส JWT โดยไม่ตรวจสอบ signature (เพราะ Cognito Access Token เป็น JWT signed)
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        
        # ดึงข้อมูล username (sub หรือ preferred_username)
        username = decoded_token.get("username") or decoded_token.get("cognito:username")
        return username
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None

class MainView(View):
    def get(self, request):
        if request.session.get('access_token'):
            access_token = request.session.get('access_token')
            username = get_username_from_access_token(access_token) if access_token else None
        else:
            username = ''
        return render(request, "index.html",{
            'username' : username
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

             # รับโทเค็นจาก Cognito
            access_token = response['AuthenticationResult']['AccessToken']
            
            # จัดเก็บ Access Token ใน session
            request.session['access_token'] = access_token
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
                messages.success(request, 'Please check your email for a confirmation code.')
                return render(request, "account/confirmemail.html",{
                    'username' : username
                })
            
            except cognito_client.exceptions.UsernameExistsException:
                messages.error(request, 'Username already exists')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
            
            return render(request, "account/signup.html")
        
class ConfirmEmail(View):
    def get(self, request):
        return render(request, "account/confirmemail.html",{
            
        })
        
    def post(self, request):
        # รับข้อมูลจากฟอร์ม
        username = request.POST.get('username')
        confirmation_code = request.POST.get('confirmation_code')

        try:
            response = cognito_client.confirm_sign_up(
                ClientId=settings.COGNITO_CLIENT_ID,
                Username=username,
                ConfirmationCode=confirmation_code,
            )
            messages.success(request, 'Email confirmed successfully! You can now log in.')
            return redirect('signin')  # เปลี่ยนไปยังหน้า login หลังยืนยันอีเมลเสร็จสิ้น
        
        except cognito_client.exceptions.CodeMismatchException:
            messages.error(request, 'Invalid confirmation code. Please try again.')
        except cognito_client.exceptions.UserNotFoundException:
            messages.error(request, 'User not found. Please check your username.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

        return render(request, "account/confirmemail.html")

class LogoutView(View):
    def get(self, request):
        # ลบ Access Token และข้อมูลการล็อกอินจาก session
        request.session.pop('access_token', None)

        messages.success(request, 'You have successfully logged out.')    
        return redirect('signin')


