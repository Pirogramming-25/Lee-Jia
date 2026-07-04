from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import get_template

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ideas:list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def main_css(request):
    template = get_template('accounts/main.css')
    css_content = template.template.source
    return HttpResponse(css_content, content_type='text/css')