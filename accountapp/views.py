from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, get_user_model, login
from .models import Profile
from .forms import ProfileForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from blogapp.models import Post


# Create your views here.
def signup(request): 
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            Profile.objects.create(user=user) 
            auth.login(request, user)
            return redirect('/')
    
    else:
        signup_form = CustomUserCreationForm()

    return render(request, 'signup.html', {'signup_form' : signup_form})
            
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, 'signin.html', {'error' : '아이디 비밀번호 확인 '})

    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('accounts:signin')

def people(request, username):
    people = get_object_or_404(get_user_model(), username=username)
    posts = Post.objects.filter(author=people)
    return render(request, 'people.html', {'people' : people, 'posts':posts})
    

def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
        return redirect('accounts:people', request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', { 'profile_form' : profile_form})

def follow(request, user_id):
    people = get_object_or_404(get_user_model(), id = user_id)
    if request.user in people.followers.all():
        people.followers.remove(request.user)
    else:
        people.followers.add(request.user)
    
    return redirect('accounts:people', people.username)