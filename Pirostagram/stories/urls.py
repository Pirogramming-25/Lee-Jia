from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('create/', views.story_create, name='story_create'),
    path('<str:username>/', views.story_detail, name='story_detail'),
]