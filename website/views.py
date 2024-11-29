from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import AddRecordForm
from .models import Record
from django.contrib.auth.models import User
from django.db.models import Q, Count, Avg, Sum, F, ExpressionWrapper, FloatField, Case, When, Value, IntegerField, Subquery, OuterRef, Window, DateField
from django.db.models.functions import TruncMonth, TruncDate, ExtractHour, ExtractYear, ExtractMonth, ExtractWeekDay, Coalesce, Lag, Cast
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from datetime import datetime, timedelta
import pandas as pd
import csv
import numpy as np
from scipy import stats
from django.utils import timezone

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {
        'form': form,
        'title': 'Register'
    })

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
    records = Record.objects.all()
    
    # Get search parameters
    search_query = request.GET.get('q', '')
    state_filter = request.GET.get('state', '')
    
    # Apply filters
    if search_query:
        records = records.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(state__icontains=search_query) |
            Q(zipcode__icontains=search_query)
        )
    
    if state_filter:
        records = records.filter(state=state_filter)
    
    # Get unique states for filter dropdown
    states = Record.objects.values_list('state', flat=True).distinct().order_by('state')
    
    # Records by state
    records_by_state = records.values('state').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Records by month
    records_by_month = records.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')
    
    context = {
        'records': records,
        'states': states,
        'current_state': state_filter,
        'search_query': search_query,
        'total_records': records.count(),
        'records_by_state': records_by_state,
        'records_by_month': records_by_month,
    }
    
    return render(request, 'dashboard_new.html', context)

@login_required
def export_records(request, format='csv'):
    records = Record.objects.all()
    
    # Convert QuerySet to list of dictionaries
    records_data = []
    for record in records:
        # Convert timezone-aware datetime to naive datetime
        created_at = record.created_at.replace(tzinfo=None) if record.created_at else None
        
        records_data.append({
            'ID': record.id,
            'First Name': record.first_name,
            'Last Name': record.last_name,
            'Email': record.email,
            'Phone': record.phone,
            'Address': record.address,
            'City': record.city,
            'State': record.state,
            'Zipcode': record.zipcode,
            'Created At': created_at
        })
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="records.csv"'
        
        writer = csv.DictWriter(response, fieldnames=records_data[0].keys())
        writer.writeheader()
        writer.writerows(records_data)
        
        return response
        
    elif format == 'excel':
        df = pd.DataFrame(records_data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="records.xlsx"'
        
        df.to_excel(response, index=False, engine='openpyxl')
        return response
        
    elif format == 'json':
        return JsonResponse(records_data, safe=False)
    
    return HttpResponse('Invalid format specified')

@login_required
def get_analytics(request):
    records = Record.objects.filter(created_by=request.user)
    
    # Get date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date and end_date:
        records = records.filter(
            created_at__range=[start_date, end_date]
        )
    
    analytics = {
        'total_records': records.count(),
        'records_by_state': list(records.values('state').annotate(
            count=Count('id')).order_by('-count')),
        'daily_trend': list(records.annotate(
            date=TruncDate('created_at')).values('date').annotate(
            count=Count('id')).order_by('date')),
        'user_stats': list(records.values('created_by__username').annotate(
            count=Count('id')).order_by('-count'))
    }
    
    return JsonResponse(analytics)

@login_required
def profile(request):
    user = request.user
    records = Record.objects.filter(created_by=user)
    
    # Get user statistics
    total_records = records.count()
    recent_records = records.order_by('-created_at')[:5]
    records_by_state = records.values('state').annotate(count=Count('id')).order_by('-count')
    
    # Calculate activity metrics
    today = datetime.now()
    last_30_days = today - timedelta(days=30)
    records_last_30_days = records.filter(created_at__gte=last_30_days).count()
    daily_average = records_last_30_days / 30 if records_last_30_days > 0 else 0
    
    context = {
        'total_records': total_records,
        'recent_records': recent_records,
        'records_by_state': records_by_state,
        'records_last_30_days': records_last_30_days,
        'daily_average': daily_average,
    }
    
    return render(request, 'profile.html', context)

@login_required
def get_user_activity_heatmap(request):
    """Get user activity heatmap data"""
    activity_data = Record.objects.annotate(
        hour=ExtractHour('created_at'),
        weekday=ExtractWeekDay('created_at')
    ).values('hour', 'weekday').annotate(
        count=Count('id')
    ).order_by('weekday', 'hour')
    
    return JsonResponse(list(activity_data), safe=False)

@login_required
def get_record_forecasts(request):
    try:
        # Get the last 30 days of records
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        records = Record.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # Convert to lists for processing
        dates = []
        counts = []
        
        # Fill in missing dates with zero counts
        current_date = start_date
        while current_date <= end_date:
            record = next((r for r in records if r['date'] == current_date), None)
            dates.append(current_date.strftime('%Y-%m-%d'))
            counts.append(record['count'] if record else 0)
            current_date += timedelta(days=1)

        # Calculate simple moving average for forecast (7-day window)
        window_size = 7
        forecast = []
        
        for i in range(len(counts)):
            if i < window_size:
                # For the first few points, use available data
                window = counts[:i+1]
                forecast.append(sum(window) / len(window))
            else:
                # Use full window size
                window = counts[i-window_size:i]
                forecast.append(sum(window) / window_size)
        
        # Add 7 days forecast
        for _ in range(7):
            next_date = (datetime.strptime(dates[-1], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            dates.append(next_date)
            last_window = forecast[-window_size:]
            next_forecast = sum(last_window) / len(last_window)
            forecast.append(next_forecast)
            counts.append(None)  # None for future dates
            
        return JsonResponse({
            'dates': dates,
            'actuals': counts,
            'forecast': forecast
        })
    except Exception as e:
        print(f"Error in get_record_forecasts: {str(e)}")  # For debugging
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_record_clusters(request):
    try:
        # Get records by state
        states = Record.objects.values_list('state', flat=True).distinct()
        
        clusters = []
        timepoints = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        for state in states:
            # Get daily pattern for each state
            pattern = [
                Record.objects.filter(
                    state=state,
                    created_at__week_day=day
                ).count()
                for day in range(1, 8)  # 1-7 for Sunday-Saturday
            ]
            
            # Normalize pattern
            if sum(pattern) > 0:
                pattern = [count/sum(pattern) * 100 for count in pattern]
            
            clusters.append({
                'state': state,
                'pattern': pattern
            })
        
        return JsonResponse({
            'clusters': clusters,
            'timepoints': timepoints
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def get_anomaly_detection(request):
    try:
        # Get the last 60 days of records
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=60)
        
        records = Record.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        # Convert to lists and fill missing dates
        dates = []
        counts = []
        
        current_date = start_date
        while current_date <= end_date:
            record = next((r for r in records if r['date'] == current_date), None)
            dates.append(current_date.strftime('%Y-%m-%d'))
            counts.append(record['count'] if record else 0)
            current_date += timedelta(days=1)

        # Calculate moving average and standard deviation
        window_size = 7
        moving_avg = []
        upper_bound = []
        lower_bound = []
        
        # Calculate baseline statistics
        for i in range(len(counts)):
            if i < window_size:
                window = counts[:i+1]
            else:
                window = counts[i-window_size:i]
            
            avg = sum(window) / len(window)
            std = np.std(window) if len(window) > 1 else 0
            
            moving_avg.append(avg)
            upper_bound.append(avg + (2 * std))
            lower_bound.append(max(0, avg - (2 * std)))

        # Detect anomalies
        anomalies = []
        anomaly_dates = []
        anomaly_counts = []
        
        for i, count in enumerate(counts):
            if count > upper_bound[i] or count < lower_bound[i]:
                anomalies.append(i)
                anomaly_dates.append(dates[i])
                anomaly_counts.append(count)

        return JsonResponse({
            'success': True,
            'data': {
                'dates': dates,
                'counts': counts,
                'moving_average': moving_avg,
                'upper_bound': upper_bound,
                'lower_bound': lower_bound,
                'anomalies': {
                    'indices': anomalies,
                    'dates': anomaly_dates,
                    'counts': anomaly_counts
                }
            }
        })
    except Exception as e:
        print(f"Error in anomaly detection: {str(e)}")  # For debugging
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def get_cohort_analysis(request):
    """Perform cohort analysis on records"""
    records = Record.objects.annotate(
        cohort_month=TruncMonth('created_at')
    ).values('cohort_month', 'state').annotate(
        count=Count('id')
    ).order_by('cohort_month')
    
    df = pd.DataFrame(records)
    if len(df) > 0:
        # Create cohort matrix
        cohort_matrix = df.pivot_table(
            values='count',
            index='cohort_month',
            columns='state',
            fill_value=0
        )
        
        # Calculate retention rates
        retention_matrix = cohort_matrix.div(cohort_matrix.sum(axis=1), axis=0) * 100
        
        return JsonResponse({
            'cohort_dates': cohort_matrix.index.astype(str).tolist(),
            'states': cohort_matrix.columns.tolist(),
            'values': retention_matrix.values.tolist()
        })
    return JsonResponse({})

@login_required
def features(request):
    return render(request, 'features.html', {
        'title': 'Features'
    })
