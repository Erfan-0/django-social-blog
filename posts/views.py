# TODO: bayad iin emkan ro faraham konam ke betoonan khodeshoon add konan yek post ro.

from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib import messages
from . import views
from.models import Post
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts':posts}) 
    

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "user is invalid")
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form':form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "invalid username or password")
        else:
            messages.error(request, "invalid form data")    
    else:
        form = AuthenticationForm()     
    return render(request, 'users/login.html', {'form':form})


def logout(request):
    auth_logout(request)
    return redirect('home')
    
@login_required                
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(author=request.user, title=title, content = content)

            return redirect('home')
        
    return render(request, 'posts/create_post.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')





