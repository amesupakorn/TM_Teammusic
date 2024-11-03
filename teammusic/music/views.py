from django.shortcuts import render, redirect
from django.views import View
from .models import *
import boto3
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import jwt
from .models import *
from django.db import transaction


cognito_client = boto3.client('cognito-idp', region_name=settings.COGNITO_REGION)


def get_username_from_access_token(access_token):
    try:
        # ถอดรหัส JWT โดยไม่ตรวจสอบ signature
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        username = decoded_token.get("username") or decoded_token.get("cognito:username")
        return username
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None

def refresh_access_token(refresh_token):
    try:
        response = cognito_client.initiate_auth(
            ClientId=settings.COGNITO_APP_CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={'REFRESH_TOKEN': refresh_token}
        )
        return response['AuthenticationResult']['AccessToken']
    except cognito_client.exceptions.NotAuthorizedException:
        return None

def get_cognito_user_id(access_token, refresh_token=None):
    try:
        response = cognito_client.get_user(AccessToken=access_token)
        for attr in response['UserAttributes']:
            if attr['Name'] == 'sub':
                return attr['Value']
    except cognito_client.exceptions.NotAuthorizedException:
        if refresh_token:
            # ขอ Access Token ใหม่ด้วย Refresh Token
            new_access_token = refresh_access_token(refresh_token)
            if new_access_token:
                # อัปเดต Access Token ใน session
                return get_cognito_user_id(new_access_token)
    return None

class MainView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        
        # ตรวจสอบ Access Token
        if access_token:
            username = get_username_from_access_token(access_token)
            cognito_user_id = get_cognito_user_id(access_token, refresh_token)
            if cognito_user_id:
                user_playlists = Playlist.objects.filter(cognito_user_id=cognito_user_id)
                has_playlists = user_playlists.exists()
            else:
                # กรณีที่ไม่สามารถดึง cognito_user_id ได้หลังจาก refresh token
                messages.error(request, 'Please Login again')
                return redirect('signin')
        else:
            username = ''
            user_playlists = []
            has_playlists = False

        # ดึงข้อมูลนักร้องและอัลบั้มทั้งหมด
        singers = Singer.objects.all()
        albums = Album.objects.all()
        
        return render(request, "index.html", {
            'username': username,
            'singer': singers,
            'album': albums,
            'user_playlists': user_playlists,
            'has_playlists': has_playlists
        })
        
class Artlist(View):
    def get(self, request, id):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        
        # ตรวจสอบ Access Token
        if access_token:
            username = get_username_from_access_token(access_token)
            cognito_user_id = get_cognito_user_id(access_token, refresh_token)
            if cognito_user_id:
                user_playlists = Playlist.objects.filter(cognito_user_id=cognito_user_id)
                has_playlists = user_playlists.exists()
            else:
                # กรณีที่ไม่สามารถดึง cognito_user_id ได้หลังจาก refresh token
                messages.error(request, 'Please Login again')
                return redirect('signin')
        else:
            username = ''
            user_playlists = []
            has_playlists = False
        
        # ดึงข้อมูลนักร้อง อัลบั้ม และเพลงทั้งหมดของนักร้องนี้
        singer = Singer.objects.get(id=id)
        albums = Album.objects.filter(singer=singer)
        songs = Song.objects.filter(album__in=albums)

        # สร้างรายการเพลง (song list) เป็น dictionary
        song_list = [
            {
                'title': song.title,
                'album': song.album.title,
                'albumCover': song.album.s3_alblumurl.url if song.album.s3_alblumurl else '',  
                'singer': singer.name,
                'songUrl': song.s3_url
            }
            for song in songs
        ]

        # ข้อมูลเพิ่มเติม เช่น จำนวนเพลง เพลงแรก และเพลงแบบสุ่ม
        countSong = songs.count()
        firstsongs = songs.first()
        songrandom = songs.order_by('?').first()

        context = {
            'username': username,
            'singer': singer,
            'albums': albums,
            'songs': songs,
            'countSong': countSong,
            'firstsongs': firstsongs,
            'songrandom': songrandom,
            'song_list': song_list,  # ส่งรายการเพลงไปยัง template
            'user_playlists': user_playlists,
            'has_playlists': has_playlists
        }

        return render(request, "artlist.html", context)
        
class Albums(View):
    
    def get(self, request, id):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        
        # ตรวจสอบ Access Token
        if access_token:
            username = get_username_from_access_token(access_token)
            cognito_user_id = get_cognito_user_id(access_token, refresh_token)
            if cognito_user_id:
                user_playlists = Playlist.objects.filter(cognito_user_id=cognito_user_id)
                has_playlists = user_playlists.exists()
            else:
                # กรณีที่ไม่สามารถดึง cognito_user_id ได้หลังจาก refresh token
                messages.error(request, 'Please Login again')
                return redirect('signin')
        else:
            username = ''
            user_playlists = []
            has_playlists = False
        
            
        album = Album.objects.get(id=id)
        songs = Song.objects.filter(album_id=id)  
        singer = album.singer  # ใช้ album.singer เพื่อดึงข้อมูลนักร้องที่เกี่ยวข้อง
        firstsongs = songs.first()
        countSong = songs.count()
        songrandom = songs.order_by('?').first()



        return render(request, "album.html",{
            'username' : username,
            'album' : album,
            'songs' : songs,
            'countSong': countSong,
            'singer' : singer,
            'firstsongs' : firstsongs,
            'songrandom': songrandom,
            'user_playlists': user_playlists,
            'has_playlists': has_playlists
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
            return render(request, "account/signin.html",{
                })
        
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
        request.session.pop('song_data', None)

        messages.success(request, 'You have successfully logged out.')    
        return redirect('signin')




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def set_song_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.session['song_data'] = {
            'title': data.get('title'),
            'album': data.get('album'),
            'albumCover': data.get('albumCover'),
            'singer': data.get('singer'),
            'songUrl': data.get('songUrl')
        }
        return JsonResponse({'message': 'Song data set in session'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_song_session(request):
    song_data = request.session.get('song_data', None)
    return JsonResponse(song_data if song_data else {'error': 'No song data in session'}, status=200)



class PlayList(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        
        # ตรวจสอบ Access Token
        if access_token:
            username = get_username_from_access_token(access_token)
            cognito_user_id = get_cognito_user_id(access_token, refresh_token)
            if cognito_user_id:
                user_playlists = Playlist.objects.filter(cognito_user_id=cognito_user_id)
                has_playlists = user_playlists.exists()
            else:
                # กรณีที่ไม่สามารถดึง cognito_user_id ได้หลังจาก refresh token
                messages.error(request, 'Please Login again')
                return redirect('signin')
        else:
            username = ''
            user_playlists = []
            has_playlists = False
      
      
        return render(request, "createPlaylist.html",{
            'username': username,
            'user_playlists': user_playlists,
            'has_playlists': has_playlists
        })


class PlayListView(View):
     def get(self, request, id):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        
        # ตรวจสอบ Access Token
        if access_token:
            username = get_username_from_access_token(access_token)
            cognito_user_id = get_cognito_user_id(access_token, refresh_token)
            if cognito_user_id:
                user_playlists = Playlist.objects.filter(cognito_user_id=cognito_user_id)
                has_playlists = user_playlists.exists()
            else:
                # กรณีที่ไม่สามารถดึง cognito_user_id ได้หลังจาก refresh token
                messages.error(request, 'Please Login again')
                return redirect('signin')
        else:
            username = ''
            user_playlists = []
            has_playlists = False
            
        playlist = Playlist.objects.get(id=id)
        song_count = playlist.songs.count()
        song = playlist.songs
        return render(request, "playlistt.html",{
            'username': username,
            'playlist' : playlist,
            'countSong': song_count,
            'songs' : song,
            'user_playlists': user_playlists,
            'has_playlists': has_playlists
        })
        
        
        

class CreatePlayList(View):    
    def post(self, request):
        
        try:
            # ดึง access token จาก session
            access_token = request.session.get('access_token')
            if not access_token:
                return JsonResponse({'success': False, 'error': 'Access token not found'}, status=400)

            # ดึง Cognito User ID จาก access token
            cognito_user_id = get_cognito_user_id(access_token)
            if not cognito_user_id:
                return JsonResponse({'success': False, 'error': 'Cognito user ID not found'}, status=400)

            # ดึงข้อมูลจาก request
            name = request.POST.get('name')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            # ตรวจสอบว่ามีการใส่ชื่อ Playlist หรือไม่
            if not name:
                return JsonResponse({'success': False, 'error': 'Playlist name is required'}, status=400)

            # สร้าง Playlist
            with transaction.atomic():
                # สร้าง Playlist
                playlist = Playlist.objects.create(
                    name=name,
                    description=description,
                    playlist_image=image,
                    cognito_user_id=cognito_user_id
                )

            
            return redirect('viewPlaylist', id=playlist.id)


        except Exception as e:
            # ดักจับข้อผิดพลาดทั้งหมดและส่งข้อความแจ้งกลับ
            return JsonResponse({'success': False, 'error': str(e)}, status=500)