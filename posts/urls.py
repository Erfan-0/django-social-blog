from django.urls import path
from . import  views


urlpatterns = [
    path('', views.home, name='home'),
    path('singup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create/', views.create_post, name='create_post')
]


