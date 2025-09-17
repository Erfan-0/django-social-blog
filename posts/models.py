from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=20) # baraye matn koochick
    summary = models.CharField(max_length=70, default="no summary provided") # age hichi nazari minevise: no summary provided
    content = models.TextField(blank=False) # baraye text haye bozorg tar. blank = khali
    created_at = models.DateTimeField(auto_now_add=True) # sabte zamane enteshare post
    updated_at = models.DateField(auto_now=True) # sabt zamane akharin update post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #expl: pedar age hazf beshe bache hasham mimiran. iinja author age hazf beshe tamame vabastegi ha az jomle post user hazf mishe(.CASCADE)  
    completed = models.BooleanField(default=False) # faghad T or F. (aya post takmil shode ya na)

#namayeshe reshte az yek shey.
# masalan be jaye Task object (1), titel oon post ro namayesh mdie (expl: amoozeshe djagno)
def __str__(self):
    return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'comments') # pedar age hazf beshe bache hasham mimiran. iinja Post age hazf beshe tamame vabastegi ha mesle comment hazf mishe. related_name= 'comments' baesh mishe ke ma betoonim iintori az tarighe post be comment ha dastresi dashte bashim: comments = Post.comments.all()       
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'comments_authored')#  nevisande commnet(ke hamoon user ma hast) hazf beshe comment hash ham hazf mishan. iinja az tarighe comment haei ke user neveshte ro mitooni beheshoon dasresi dashte bashi iintori: user.comments_authored.all()                                     
    content = models.TextField(max_length=3000) # text feilld, baraye matn haye nesbatan bozorg
    created_at = models.DateTimeField(auto_now_add=True) # modat zamane ijad shodane yek post ro migire va oon ro ba "auto_now_add=True" auto add mikone  

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}" # az author, username ro migire va neshoon mide



def __str__(self):
    return self.username # ASK MOHSEN, IDKRN

# iin code bayad barresi beshe. chera baraye user az OneToOneField estefade mishe? IDKRN
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # baraye rabete yek be yek estefade mishe. masalan ForegienKey mige: yek nevisande mitoone chand post dashte bashe. OneToOneField mige: yek karbar faghat yek profile dare


    def __str__(self):
        return self.user.username # ASK MOHSEN, IDKRN


from django.apps import AppConfig # AppConfig mesle modire yek sakhtemoone ke mitoone App ro midiriyat kone

# iin class baraye iine ke app betoone modiriyat beshe bad az har taghiri(ex: user vared shod, folan kar ro bokon, post sakhte shod, folan kar ro bokon va...)
class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # iin khodesh miyad Primary key ro auto auto add mikone 
    name = 'users' # iin yek esme baraye iine ke Django befahme iin yek iin tanzimati ke modire sakhtemoon(AppConfig) marboot ke kodoom app hast

    def ready(self): # djagno vaghti app ro kamel bargozari kard iin tabe ro seda mizane, yani vaghti hame chiz tamoosh shod iinja mitooni ye kari anjam bedi. masalan ma tooye khate badi bebin chi goftim
        import users.signals #  iinja goftim ke bad ke App kare khodesh ro anjam dad, signals.py ejra beshe ke age beri bebini, marboot be sakhte profile baraye user hast 






