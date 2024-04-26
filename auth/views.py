from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def log_in(request):
    if request.method == 'POST':  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('dashboard:index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    return render(request, 'auth/login.html')


def log_out(request):
    logout(request)
    messages.success(request, 'logout success')
    return redirect('auth:login')
