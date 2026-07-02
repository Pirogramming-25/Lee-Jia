from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'reviews/movie_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'reviews/movie_detail.html', {'movie': movie})

def movie_create(request):
    if request.method == 'POST':
        Movie.objects.create(
            title=request.POST.get('title'),
            release_year=request.POST.get('release_year'),
            director=request.POST.get('director'),
            actors=request.POST.get('actors'),
            genre=request.POST.get('genre'),
            rating=request.POST.get('rating'),
            runtime=request.POST.get('runtime'),
            review=request.POST.get('review'),
        )
        return redirect('movie-list')
    return render(request, 'reviews/movie_form.html')

def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.release_year = request.POST.get('release_year')
        movie.director = request.POST.get('director')
        movie.actors = request.POST.get('actors')
        movie.genre = request.POST.get('genre')
        movie.rating = request.POST.get('rating')
        movie.runtime = request.POST.get('runtime')
        movie.review = request.POST.get('review')
        movie.save()
        return redirect('movie-detail', pk=pk)
    return render(request, 'reviews/movie_form.html', {'movie': movie})

def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movie-list')