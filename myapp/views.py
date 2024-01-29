from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .form import CreateUserForm
import pyrebase

config= {
  'apiKey': "AIzaSyBTroOFetBp-dswbgn5ybGnQ_8T0X-eLS4",
  'authDomain': "coba-8058c.firebaseapp.com",
  'databaseURL': "https://coba-8058c-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "coba-8058c",
  'storageBucket': "coba-8058c.appspot.com",
  'messagingSenderId': "1082277137265",
  'appId': "1:1082277137265:web:68acd180fb28370bcec4d0",
  "measurementId": "G-5MQ0Y7Y8Z2"
}

firebase= pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()


# Create your views here.


def index(request):
    return render(request, 'index.html', {'request':request})

# def pretty_request(request):
#     headers = ''
#     for header, value in request.META.items():
#         if not header.startswith('HTTP'):
#             continue
#         header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
#         headers += '{}: {}\n'.format(header, value)

#     return (
#         '{method} HTTP/1.1\n'
#         'Content-Length: {content_length}\n'
#         'Content-Type: {content_type}\n'
#         '{headers}\n\n'
#         '{body}'
#     ).format(
#         method=request.method,
#         content_length=request.META['CONTENT_LENGTH'],
#         content_type=request.META['CONTENT_TYPE'],
#         headers=headers,
#         body=request.body,
#     )

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        userfire = auth.sign_in_with_email_and_password(email, password)
        session_id=userfire['idToken']
        request.session['uid']= str(session_id)
        print(userfire)
        request.user.is_authenticated=True
        return redirect('/')
    context={
        "request":request
    }
    return render(request, 'login.html')

def registerUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password1")
        user= auth.create_user_with_email_and_password(email, password)
        return redirect('login')


    context={
        "form": form
    }
    
    return render(request, 'register.html',context)