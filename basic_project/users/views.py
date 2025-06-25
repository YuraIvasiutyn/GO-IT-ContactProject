from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='main')
        else:
            print(":x: Signup Form Errors:", form.errors)  # :point_left: Додай для дебагу
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='basic_project:main')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is None:
                messages.error(request, 'Username or password didn\'t match')
                return redirect(to='users:login')
            login(request, user)
            return redirect(to='main')
        else:
            print(form.errors)
    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='main')










