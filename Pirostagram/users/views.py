from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .forms import SignupForm, ProfileEditForm
from .models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user)
    is_following = request.user.following.filter(id=profile_user.id).exists()
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
@require_POST
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return JsonResponse({'error': '자기 자신은 팔로우 불가'}, status=400)

    if request.user.following.filter(id=target.id).exists():
        request.user.following.remove(target)
        is_following = False
    else:
        request.user.following.add(target)
        is_following = True

    return JsonResponse({
        'is_following': is_following,
        'follower_count': target.followers.count(),
    })

@login_required
def user_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | Q(name__icontains=query)
        ).exclude(id=request.user.id)
    return render(request, 'users/search.html', {
        'query': query,
        'results': results,
    })