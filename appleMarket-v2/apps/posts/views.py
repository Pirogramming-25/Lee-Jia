import os
import tempfile

# [중요] Paddle 실행 버그 방지 환경 변수
os.environ['FLAGS_enable_pir_api'] = '0'
os.environ['FLAGS_use_mkldnn'] = '0'

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Post
from .forms import PostForm
from .services.ocr_service import extract_text_from_image
from .services.rules import parse_nutrition

def main(request):
    posts = Post.objects.all()
    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if search_txt:
        posts = posts.filter(title__icontains=search_txt)
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass
    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)


def create(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')


def detail(request, pk):
    target_post = Post.objects.get(id=pk)
    return render(request, 'posts/detail.html', {'post': target_post})


def update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'posts/update.html', {'form': form, 'post': post})
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:detail', pk=pk)


def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')


# ---------- OCR API ----------
@require_POST
def analyze_nutrition(request):
    """AJAX 요청: 영양성분표 이미지를 받아 OCR 후 파싱하여 JSON 반환"""
    if 'nutrition_image' not in request.FILES:
        return JsonResponse({'success': False, 'error': '이미지가 없습니다.'}, status=400)

    uploaded = request.FILES['nutrition_image']

    # 확장자 유지하며 임시 파일 저장
    suffix = os.path.splitext(uploaded.name)[1] or '.jpg'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in uploaded.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        texts = extract_text_from_image(tmp_path)
        nutrition = parse_nutrition(texts)
        return JsonResponse({
            'success': True,
            'nutrition': nutrition,
            'raw_texts': texts,  # 디버깅용 (프론트에서 안 써도 됨)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)