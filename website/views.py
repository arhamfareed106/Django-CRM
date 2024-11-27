from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    # Check if the request is a POST (login attempt)
    if request.method == 'POST':
        # Extract username and password from the form
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log in the user and display a success message
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')  # Redirect to the home page or any other route
        else:
            # Display an error message for invalid credentials
            messages.error(request, 'Invalid username or password.')
    else:
      return render(request, 'home.html', {})
def login_user(request):
    pass

def logout_user(request):
  pass