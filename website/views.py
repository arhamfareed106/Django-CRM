from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.contrib.auth.models import User
from django.db.models import Q, Count
import csv
from django.http import HttpResponse
from datetime import datetime
from django.db.models.functions import TruncMonth

def home(request):
    records = Record.objects.all()
    
    # Get counts for dashboard
    if request.user.is_authenticated:
        recent_count = Record.objects.filter(
            created_at__isnull=False
        ).order_by('-created_at')[:5].count()
        
        # Count unique states
        state_count = Record.objects.values('state').distinct().count()
    else:
        recent_count = 0
        state_count = 0
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "Error logging in. Please try again.")
            return redirect('home')
    
    return render(request, 'home.html', {
        'records': records,
        'recent_count': recent_count,
        'state_count': state_count,
    })

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@login_required
def customer_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    return render(request, 'record.html', {'record': record})

@login_required
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if record.created_by == request.user:
        record.delete()
        messages.success(request, "Record deleted successfully!")
    else:
        messages.error(request, "You can only delete your own records!")
    return redirect('home')

@login_required
def add_record(request):
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            messages.success(request, "Record added successfully!")
            return redirect('home')
    else:
        form = AddRecordForm()
    return render(request, 'add_record.html', {'form': form})

@login_required
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if record.created_by != request.user:
        messages.error(request, "You can only update your own records!")
        return redirect('home')
    
    if request.method == 'POST':
        form = AddRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('home')
    else:
        form = AddRecordForm(instance=record)
    return render(request, 'update_record.html', {'form': form})

@login_required
def dashboard(request):
    records = Record.objects.filter(created_by=request.user)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        records = records.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        )
    
    # Filter functionality
    state_filter = request.GET.get('state')
    if state_filter:
        records = records.filter(state=state_filter)
    
    # Get statistics for dashboard
    total_records = records.count()
    records_by_state = records.values('state').annotate(count=Count('id'))
    records_by_month = records.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'records': records,
        'total_records': total_records,
        'records_by_state': records_by_state,
        'records_by_month': records_by_month,
        'states': Record.objects.values_list('state', flat=True).distinct(),
    }
    return render(request, 'dashboard.html', context)

@login_required
def export_records_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="records_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Address', 'City', 'State', 'Created At'])
    
    records = Record.objects.filter(created_by=request.user).values_list(
        'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'created_at'
    )
    
    for record in records:
        writer.writerow(record)
    
    return response

@login_required
def profile(request):
    user = request.user
    records_count = Record.objects.filter(created_by=user).count()
    recent_records = Record.objects.filter(created_by=user).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'records_count': records_count,
        'recent_records': recent_records,
    }
    return render(request, 'profile.html', context)
