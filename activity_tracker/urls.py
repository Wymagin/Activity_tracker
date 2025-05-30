"""
URL configuration for activity_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'activity_tracker'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base_view, name='base'),
    path('home/', views.home_view, name='home'),
    path('register/', views.sign_up, name='register'),
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-activity/', views.add_activity, name='add_activity'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/day/', views.dashboard_day_view, name='dashboard_day'),
    path('dashboard/week/', views.dashboard_week_view, name='dashboard_week'),
    path('dashboard/month/', views.dashboard_month_view, name='dashboard_month'),
]


