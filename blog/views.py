from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post

def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # title = form.cleaned_data['title']
            # content = form.cleaned_data['content']
            # write the data into database
            form.save()
            
    form = PostForm()
    posts = Post.objects.all().order_by('-date_posted')
    context = {
        'form': form,
        'posts': posts
        }
    return render(request, 'blog/home.html', context)

def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit.html', {'form': form})

def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if 'delete' in request.POST:
            post.delete()
            return redirect('home')
        else:
            return redirect('home')
    else:
        return render(request, 'blog/delete.html', {'post': post})
