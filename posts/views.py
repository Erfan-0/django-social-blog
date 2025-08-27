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
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm




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
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(title=title, summary = summary, content = content, author=request.user)
            messages.success(request,"post created successfully!")
            return redirect('profile')
        
    return render(request, 'posts/create_post.html')

def post_details(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post_detail.html', {'post':post})

@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'users/profile.html', {'user_posts': user_posts})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.summary = request.POST.get('summary')
        post.content = request.POST.get('content')
        post.save()
        messages.success(request, "Post updated successfully!")
        return redirect('profile')
    
    return render(request, 'posts/edit_post.html', {'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return HttpResponse("You are not allowed to delete this post")

    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('profile')


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {'post': post, 'form': form})            