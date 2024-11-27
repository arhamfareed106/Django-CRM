from django.urls import path
from . import views  # Ensure views.py exists in the same directory as urls.py

urlpatterns = [
    path('', views.home, name='home'),  # Home page # type: ignore
    # path('login/', views.login_user, name='login'),  # Login page
    path('logot/', views.logout_user, name='logout'),  # Logout page
]
