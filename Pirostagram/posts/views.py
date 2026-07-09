import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import Post, Comment
from .forms import PostForm

User = get_user_model()


@login_required
def post_list(request):
    # 팔로우한 사람 + 나 자신의 게시글만
    following_users = request.user.following.all()
    author_pool = list(following_users) + [request.user]
    posts = Post.objects.filter(author__in=author_pool)

    # 스토리 있는 유저만
    story_users = [u for u in author_pool if u.stories.exists()]

    # 우측 추천 유저 (내가 안 팔로우한 사람)
    suggested = User.objects.exclude(
        id__in=[request.user.id] + [u.id for u in following_users]
    )[:5]

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'story_users': story_users,
        'suggested': suggested,
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'mode': 'create'})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'mode': 'update'})

@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return JsonResponse({'success': True, 'post_id': pk})

@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

@login_required
@require_POST
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = json.loads(request.body)
    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'error': '내용을 입력하세요'}, status=400)

    comment = Comment.objects.create(post=post, author=request.user, content=content)
    return JsonResponse({
        'success': True,
        'comment_id': comment.id,
        'author': comment.author.username,
        'content': comment.content,
    })


@login_required
@require_POST
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    data = json.loads(request.body)
    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'error': '내용을 입력하세요'}, status=400)
    comment.content = content
    comment.save()
    return JsonResponse({'success': True, 'content': comment.content})


@login_required
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    comment.delete()
    return JsonResponse({'success': True, 'comment_id': pk})