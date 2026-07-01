from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.movie_list, name='movie-list'),
    path('review/create/', views.movie_create, name='movie-create'),
    path('review/<int:pk>/', views.movie_detail, name='movie-detail'),
    path('review/<int:pk>/update/', views.movie_update, name='movie-update'),
    path('review/<int:pk>/delete/', views.movie_delete, name='movie-delete'),
]