from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=20) # baraye matn koochick
    summary = models.TextField(100, default="no summary provided")
    content = models.TextField(blank=False) # baraye text haye bozorg tar. blank = khali
    created_at = models.DateTimeField(auto_now_add=True) # sabte zamane enteshare post
    updated_at = models.DateField(auto_now=True) # sabt zamane akharin update post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #expl: pedar age hazf beshe bache hasham mimiran. iinja User age hazf beshe tamame vabastegi ha az jomle post user hazf mishe.
    completed = models.BooleanField(default=False) # faghad T or F. (aya post takmil shode ya na)

#namayeshe reshte az yek shey.
# masalan be jaye Task object (1), titel oon post ro namayesh mdie (expl: amoozeshe djagno)
def __str__(self):
    return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'comments') # pedar age hazf beshe bache hasham mimiran. iinja Post age hazf beshe tamame vabastegi ha mesle comment hazf mishe. related_name= 'comments' baesh mishe ke ma betoonim iintori az tarighe post be comment ha dastresi dashte bashim: comments = Post.comments.all()       
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'comments_authored')# mesle line balaei. ba iin tafavot ke iinja az tarighe comment haei ke user neveshte ro mitooni beheshoon dasresi dashte bashi iintori: user.comments_authored.all()                                     
    content = models.TextField(max_length=3000) # text feilld, baraye matn haye nesbatan bozorg
    title = models.TextField(max_length=200) # '''
    created_at = models.DateTimeField(auto_now_add=True) # modat zamane ijad shodane yek post ro migire va oon ro ba "auto_now_add=True" auto add mikone  

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}" # az author, username ro migire va neshoon mide

class User(models.Model):
    username = models.CharField(max_length=25) # username
    password = models.CharField(max_length=200) # password  
    email = models.EmailField(max_length=200, null=True) # email: mitoone khali bashe
    

def __str__(self):
    return self.username # ASK MOHSEN, IDKRN

# iin code bayad barresi beshe. chera baraye user az OneToOneField estefade mishe? IDKRN
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # baraye rabete yek be yek estefade mishe. masalan ForegienKey mige: yek nevisande mitoone chand post dashte bashe. OneToOneField mige: yek karbar faghat yek profile dare


    def __str__(self):
        return self.user.username # ASK MOHSEN, IDKRN


from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals






