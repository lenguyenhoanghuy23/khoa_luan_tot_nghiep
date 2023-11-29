from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import *

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'đăng nhập không thành công')
    return render(request, 'accounts/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        # print(username,email,phone,password,repassword)
        if password == repassword:
            if User.objects.filter(username=username).exists():
                print("tai khoan ton tai")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    print("email ton tai")
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    data = Customer(user=user, phone_field=phone)
                    data.save()

                    # our_user = authenticate(
                    #     username=username, password=password)
                    # if our_user is not None:
                    #     login(request, user)
                    return redirect('/')
        else:
            print('loi o day')
            return redirect('register')
    return render(request, 'accounts/register.html')


def user_logout(request):
    logout(request)
    return redirect('index')
