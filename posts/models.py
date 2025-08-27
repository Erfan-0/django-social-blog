from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=20) # baraye matn koochick
    summary = models.TextField(100, default="no summary provided")
    content = models.TextField(blank=False) # baraye text haye bozorg tar. blank = khali
    created_at = models.DateTimeField(auto_now_add=True) # sabte zamane enteshare post
    updated_at = models.DateField(auto_now=True) # sabt zamane akharin update post
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    completed = models.BooleanField(default=False) # faghad T or F. (aya post takmil shode ya na)

#namayeshe reshte az yek shey.
# masalan be jaye Task object (1), titel oon post ro namayesh mdie (expl: amoozeshe djagno)
def __str__(self):
    return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'comments_authored')
    content = models.TextField(max_length=450)
    title = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"

class User(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=200)                 
    email = models.EmailField(max_length=200, null=True)
    

def __str__(self):
    return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_imgages')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals






