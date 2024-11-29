from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export_records/<str:format>/', views.export_records, name='export_records'),
    path('analytics/', views.get_analytics, name='get_analytics'),
    path('profile/', views.profile, name='profile'),
    path('get_user_activity_heatmap/', views.get_user_activity_heatmap, name='get_user_activity_heatmap'),
    path('get_record_forecasts/', views.get_record_forecasts, name='get_record_forecasts'),
    path('get_record_clusters/', views.get_record_clusters, name='get_record_clusters'),
    path('get_anomaly_detection/', views.get_anomaly_detection, name='get_anomaly_detection'),
    path('get_cohort_analysis/', views.get_cohort_analysis, name='get_cohort_analysis'),
    path('get_record_forecasts/', views.get_record_forecasts, name='get_record_forecasts'),
    path('get_record_clusters/', views.get_record_clusters, name='get_record_clusters'),
    path('get_anomaly_detection/', views.get_anomaly_detection, name='get_anomaly_detection'),
]
