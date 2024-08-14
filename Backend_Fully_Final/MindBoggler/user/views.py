from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from passlib.hash import pbkdf2_sha256
from .models import UserManager,Book 
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required  
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from retriver import giveBooks
# Create your views here.
# Create your views here.

def signup(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        location = request.POST.get("location")
        age = request.POST.get("age")
        password = pbkdf2_sha256.encrypt(password,rounds=12000,salt_size=32)
        if UserManager.objects.filter(username=username).exists():
            # return HttpResponse("User already exists")
            return render(request,"signup.html",{"Error":"User already exists"})
        else:
            user = UserManager(username=username,password=password,location=location,age=age)
            user.save()
            return HttpResponse("User created")
    return render(request,"signup.html")

def login_view(request):
    error = False
    if request.method=="POST":
        username =request.POST.get("username")
        password = request.POST.get("password")
        if UserManager.objects.filter(username=username).exists():
            user = UserManager.objects.get(username=username)
            if pbkdf2_sha256.verify(password,user.password):
                user2=None
                if User.objects.filter(username=username).exists()==False:
                    user2 = User.objects.create_user(username=username,password=password)
                    user2.save()
                else:
                    user2 = User.objects.get(username=username)
                login(request,user2)
                return redirect("/user/home/")
            else:
                error = True
        if error:
            params={"Error":"Invalid Credentials"}
            return render(request,"frontend/login2.html",params)
    
    return render(request,"frontend/login2.html")


@login_required(login_url="/user/login/")
def home(request):
    check_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    if check_ajax:
        if request.method=="POST":
            if(len(request.body)==0):
                print("POST REQUEST")
                book_names = Book.objects.all().order_by('title').values_list('title', flat=True)
                print(len(book_names))
                book_names = list(book_names)
                return JsonResponse({'Status':'Done','Books':book_names},status=200)
            else:
                print("Search Request")
                data = json.loads(request.body)
                book_name = data.get('book_name')
                print("Book Name = ",book_name)
                book_url = Book.objects.filter(title=book_name).values_list('image_m', flat=True).first()
                recommend = giveBooks(50,50,book_name,5)
                print("Recommended = ",recommend)
            return JsonResponse({'Status':'Done','Books':book_url,'recomm':recommend},status=200)
        else:
            return JsonResponse({'Status':'Failed','Books':[]},status=400)
    return render(request,"frontend/index2.html")
   
@login_required(login_url="/user/login/")
def logout_view(request):
    logout(request)
    return HttpResponse("Logged out")