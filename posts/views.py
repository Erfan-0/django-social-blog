from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
    posts = Post.objects.all().order_by('-created_at') # hame post ha ro migigre az Post va be tartin jadid tarin ha ro neshoon mide".order_by('-created_at')"
    return render(request, 'posts/post_list.html', {'posts':posts}) # post haei ke gerefte shodan, tooye file html neshooon dade mishan. {'posts':posts} baraye iine ke ma betoonim post ha ro tooye file html tarif konim. mesle (post.title)

# GET: safhe website be daste user reside va oon ro dide vali hanooz chizi ersal nakarde
# POST : vaghti ke form ersal shode (masalan dokme signup ro zade va form ro ersal karde)
def signup(request):
    if request.method == 'POST': # age user dokme signup ro zad(form ersal karde bood(form zamani ejra mishe ke user feild haye marboot be signup kardan ro dorost por karde bashe va taeid shode bashe)) iin etefagh miyofte:
        form = UserCreationForm(request.POST) # iin form ma hast. UserCrationForm form amade khode django hast ke chiz haei mesle username, password va... ro dar khodesh dare ma iinja tooye (request.POST) migi oon chiz haei ke dari mesle username, possword va... ro barabar gharar bede be oon chizi ke user vared karde. va hala dige form ma takmil mishe vali hanooz check nashode ke bebinim dorost por karde ya na. berim khate bad bebinim 
        if form.is_valid(): # iinja check mishe aya etelaate form dorost va motabare ya na(masalan aya form kamel hast?, password ghavi hast? username tekrari nist?)
            user = form.save() # age form motabar bashe user jadid ro save mikone tooye data base
            login(request, user) # iin khat baes mishe ke niyaz nabashe user bad az singuo bere login kone. khodesh login ro barash anjam mide!
            return redirect('home') # bad az hame iin kar ha. iin khat az code, user ro be home hedayat mikone
        else:
            messages.error(request, "user is invalid") # error dar soorate invalid boodane user
    else: # yani dar soorati ke request.method == 'GET' bashe(GET hame ke goftam. user safhe ro bebine tooye GET hast. chizi ersal kone mishe POST)
        form = UserCreationForm() # age user hanooz form ro nafrestade(request.method karbar barabar ba POST nabashe) miyad form khali ijad mikone ke user poresh kone va singup bokone
    return render(request, 'users/signup.html', {'form':form}) # che form valid bashe che invalid, signup.html ro neshoon mide ke gahleb ha namayesh dade beshan va user form ha ro bebine


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