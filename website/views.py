from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Handles login and displays the home page
def home(request):
    if request.method == 'POST':
        # Extract username and password
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')  # Redirect to home or any other page
        else:
            messages.error(request, 'Invalid username or password.')

    # Render the home page
    return render(request, 'home.html')

# Handles logout functionality
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

# Placeholder for custom login (optional)
def login_user(request):
    return redirect('home')
