from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import SignUpForm, SignInForm, BlogForm

# Create your views here.
def home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'blogs': blogs})

def signup(request):
    if request.user.is_authenticated:
        return redirect("/profile")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/profile')
    else:
        form = SignUpForm()
    return render(request, 'form.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("/profile")
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile')
    else:
        form = SignInForm()
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/signin')
def profile(request):
    blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'blogs': blogs})

@login_required(login_url='/signin')
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('/profile')
    else:
        form = BlogForm()
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/signin')
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/signin')
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    blog.delete()
    return redirect('/profile')

@login_required(login_url='/signin')
def user_logout(request):
    logout(request)
    return redirect('/')