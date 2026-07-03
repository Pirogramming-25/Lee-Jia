from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Idea, IdeaStar
from .forms import IdeaForm

def idea_list(request):
    sort = request.GET.get('sort', 'new')
    ideas = Idea.objects.all()
    if sort == 'name':
        ideas = ideas.order_by('title')
    elif sort == 'old':
        ideas = ideas.order_by('created_at')
    elif sort == 'star':
        ideas = ideas.annotate(star_count=Count('stars')).order_by('-star_count')
    else:
        ideas = ideas.order_by('-created_at')

    if request.user.is_authenticated:
        starred_ids = set(IdeaStar.objects.filter(user=request.user).values_list('idea_id', flat=True))
    else:
        starred_ids = set()

    return render(request, 'ideas/idea_list.html', {
        'ideas': ideas,
        'sort': sort,
        'starred_ids': starred_ids,
    })

def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('ideas:detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_form.html', {'form': form, 'mode': 'create'})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    is_starred = False
    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    return render(request, 'ideas/idea_detail.html', {'idea': idea, 'is_starred': is_starred})

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('ideas:detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/idea_form.html', {'form': form, 'mode': 'update'})

def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('ideas:list')

@login_required
def idea_star_toggle(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    star, created = IdeaStar.objects.get_or_create(user=request.user, idea=idea)
    if not created:
        star.delete()
        starred = False
    else:
        starred = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'starred': starred, 'count': idea.stars.count()})
    return redirect(request.META.get('HTTP_REFERER', 'ideas:list'))

def idea_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    direction = request.GET.get('dir')
    if direction == 'up':
        idea.interest += 1
    elif direction == 'down':
        idea.interest -= 1
    idea.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'interest': idea.interest})
    return redirect(request.META.get('HTTP_REFERER', 'ideas:list'))