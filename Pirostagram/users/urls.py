from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('search/', views.user_search, name='search'),
    path('edit/profile/', views.profile_edit_view, name='profile_edit'),

    path('<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('<str:username>/', views.profile_view, name='profile'),
]