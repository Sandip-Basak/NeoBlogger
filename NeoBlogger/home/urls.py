from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('logout/', views.user_logout, name='logout'),
]
