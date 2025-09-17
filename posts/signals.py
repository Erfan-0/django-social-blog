from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile



@receiver(post_save, sender=User)
def create_profile(instance, created): # created = True OR False. isntance = Useri ke sabtename mikone
    if created:
        Profile.objects.create(user = instance) # iija daghighan miyad yek profile baray user jadid misaze

# iinja user age taze vared beshe ya profile ro edit kone save mikone oon ro.
@receiver(post_save, sender=User)      
def save_profile(instance): # instance = User
    instance.profile.save() # iinja hamoon jaei hast ke profile ro save mikone



      