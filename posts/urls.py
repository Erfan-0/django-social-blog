from django.urls import path
from . import  views


urlpatterns = [
    path('', views.home, name='home'),
    path('singup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_details, name='post_detail'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment')
]





