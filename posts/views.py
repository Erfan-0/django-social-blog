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
            user = form.save() # jalebe begam ke iinjast ke khodesh password ro hash shode save imkone. age form motabar bashe user jadid ro save mikone tooye data base
            login(request, user) # iin khat baes mishe ke niyaz nabashe user bad az singuo bere login kone. khodesh login ro barash anjam mide!
            return redirect('home') # bad az hame iin kar ha. iin khat az code, user ro be home hedayat mikone
        else:
            messages.error(request, "user is invalid") # error dar soorate invalid boodane user
    else: # yani dar soorati ke request.method == 'GET' bashe(GET hame ke goftam. user safhe ro bebine tooye GET hast. chizi ersal kone mishe POST)
        form = UserCreationForm() # age user hanooz form ro nafrestade(request.method karbar barabar ba POST nabashe) miyad form khali ijad mikone ke user poresh kone va singup bokone
    return render(request, 'users/signup.html', {'form':form}) # che form valid bashe che invalid, signup.html ro neshoon mide ke gahleb ha namayesh dade beshan va user form ha ro bebine

# ASK MOHSEN: AuthenticationForm farghesh ba form.is_vali chiye? mage har dotashooon marboot ke iinke check konan bebinan username va password user ba chizi ke tooye db hast barabar hastan ya na?
def login_page(request):
    if request.method == 'POST': # age user form ersal karde bood
        form = AuthenticationForm(request, data=request.POST) # AuthenticationForm yek form amade shode Django hast ke etelaate form ke tooye data base hast ro check mikone bebine yeki hastan va hamkhooni daran ya na. "data=request.POST" iinja dataei ke bayad barresi beshe ro barabr gharar dadim be etelaati ke user POST mikone baramoon
        if form.is_valid(): # valid boodane formi ke user ersal karde
            username = form.cleaned_data.get('username') # ASK MOHSEN
            password = form.cleaned_data.get('password') # ASK MOHSEN
            user = authenticate(username=username, password=password) # iinja djagno barresi mikone ke aya username va password kham ke user neveshte ba password hash shode  dakhele db hamkhooni dare ya na. age hamahang bashe ye shey barmigardoone(iintori: <User: erfan>, Password: HASH PASSWORD. hata barreso mikone ke iin user staff hast ya na) barmigardoone. age hamahang nabashe None barmigardoone
            if user is not None: # age user(hamoon user ke too khate bala tarif kardim) motabar bood(None nabashe yani ye shey bargardoonde va motabare)
                login(request, user) # session baraye user misaze 
                next_url = request.GET.get('next') # age user login nakarde bashe va bekhad kari ro anjam bede ke be login kardan niyaz dare(mesle sakhte post). django miyad masalan url ro iintori mikone: "/login/?next=/create/" yani mibaratesh be login page ke aval login kone badesh mibaratesh be oon url ke user ghabl az login kardan darkhast karde bood(/create)           
                if next_url: # agar next_url vojood dasht
                    return redirect(next_url) # ye jooraei mige: hala ke vared shodi, befarma iinam hamoonjaei ke mikhasti beri
                return redirect('home') # iin dar soorati etefagh miyofte ke next_url vojood nadashte bashe va user mostaghim oomade ke login kone. pas bad az iinke login kard redirectesh mikonim be 'home'
            else: # age None bood(invalid bood)
                messages.error(request, "invalid username or password") # error
        else: # yani dar soorati ke request.method == 'GET' bashe
            messages.error(request, "invalid form data")  # error dar soorate invalid boodane form  
    else: # yani dar soorati ke 
        form = AuthenticationForm() # agar hanooz formi ijad nashode, form khali mifreste user oon ro por kone 
    return render(request, 'users/login.html', {'form':form}) # che form valid bashe che invalid, login.html ro neshoon mide ke gahleb ha namayesh dade beshan va user form ha ro bebine


def logout(request):
    auth_logout(request) # auth_logout, tabe amade django hast ke miyad session user ro pak mikone va iin baes mishe ke logout kone 
    return redirect('home')

@login_required # be iin migim decorator. be iin mani ke faghat user haei ke login kardan mitoonan iin safhe ro bebinan. age kasi login nakarde bashe django khodesh mifrestatesh be safhe vorood ke login kone                 
def create_post(request):
    if request.method == 'POST': # age user ye form ro ersal kard
        title = request.POST.get('title') # title ro az form html migire va = title garar mide
        summary = request.POST.get('summary') # get summary from html form
        content = request.POST.get('content') # get content from html form
        if title and content: # agar title va content vojood dashtand. summary ham chon ekhtiyariye check nemishe
            Post.objects.create(title=title, summary = summary, content = content, author=request.user) # post ro misaze va meghdar haei ke dare ro barabar gharar mide ba chiz haei ke user vared karde
            messages.success(request,"post created successfully!") # success message bad az sakhte post
            return redirect('profile') # bad az sakhte post ma iinja user ro be safhe marboot be profile redirect mikonim
        
    return render(request, 'posts/create_post.html') # be mahze erjar shodane iin tabe ma hamzaman create_post.html ham neshoon dade mishe ke ghaleb vojood dashte bashe va beshe did 

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