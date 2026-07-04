from django.shortcuts import render, redirect, get_object_or_404
from .models import DevTool
from .forms import DevToolForm

def devtool_list(request):
    devtools = DevTool.objects.all().order_by('-created_at')
    return render(request, 'devtools/devtool_list.html', {'devtools': devtools})

def devtool_create(request):
    if request.method == 'POST':
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtools:detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, 'devtools/devtool_form.html', {'form': form, 'mode': 'create'})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    return render(request, 'devtools/devtool_detail.html', {'devtool': devtool})

def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == 'POST':
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect('devtools:detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'devtools/devtool_form.html', {'form': form, 'mode': 'update'})

def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('devtools:list')