from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Story, StoryImage

User = get_user_model()


@login_required
def story_create(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            story = Story.objects.create(author=request.user)
            for img in images:
                StoryImage.objects.create(story=story, image=img)
            return redirect('posts:post_list')
    return render(request, 'stories/story_form.html')


@login_required
def story_detail(request, username):
    story_user = get_object_or_404(User, username=username)
    story = story_user.stories.first()
    if not story:
        return redirect('posts:post_list')
    return render(request, 'stories/story_detail.html', {
        'story': story,
        'story_user': story_user,
    })