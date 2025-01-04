from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ActivityForm
from django.utils import timezone
from django.db.models import Sum, Count
from .models import Activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .utils import create_daily_activities_chart, create_activities_by_type_chart

# def base_view(request):
#     return render(request, 'activity_tracker/base.html', {
#         'title': 'Activity Tracker',
#         'welcome_message': 'Track and Manage Your Activities',
#     })

def base_view(request):
    return redirect('home')
    
def home_view(request):
    form = ActivityForm()
    context = {
    'form': form,
    }
    return render(request, 'activity_tracker/home.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'activity_tracker/register.html', {'form': form})


class login_view(LoginView):
    template_name = 'activity_tracker/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user  
            activity.save()
            messages.success(request, "Activity added successfully!")
        else:
            messages.error(request, "There was an error in your form. Please fix it and try again.")
    return redirect('dashboard') 

@login_required
def dashboard_view(request):
    # Get yearly activities
    period = request.GET.get('period', 'year')
    today = timezone.now().date()
    this_year = timezone.now().date().replace(month=1, day=1)
    today_activities = Activity.objects.filter(
        user=request.user, 
        start_time__date=today
    ).order_by('-start_time')
    
    # Create a default activity if none exist
    if not today_activities.exists():
        Activity.objects.create(
            user=request.user,
            name='Hello',
            activity_type='Hobby',
            start_time=timezone.now(),
            description="Thank you for visiting our site today"
        )
        today_activities = Activity.objects.filter(
            user=request.user, 
            start_time__date=today
        ).order_by('-start_time')
    
    # Tag-based statistics for the whole year
    tag_stats = Activity.objects.filter(
        user=request.user, 
        start_time__date__gte=this_year
    ).values('activity_type') \
     .annotate(
         total_duration=Sum('duration'),
         activity_count=Count('id')
     )

    daily_activities_chart = create_daily_activities_chart(request.user)
    activities_by_type_chart = create_activities_by_type_chart(request.user, period)
    form = ActivityForm()
    
    context = {
        'today_activities': today_activities,
        'tag_stats': tag_stats,
        'daily_activities_chart': daily_activities_chart,
        'activities_by_type_chart': activities_by_type_chart,
        'form': form,
        'selected_period': period,
    }
    
    return render(request, 'activity_tracker/dashboard.html', context)


@login_required
def dashboard_day_view(request):
    today = timezone.now().date()
    today_activities = Activity.objects.filter(
        user=request.user, 
        start_time__date=today
    ).order_by('-start_time')
    
    tag_stats = Activity.objects.filter(
        user=request.user, 
        start_time__date=today
    ).values('activity_type') \
     .annotate(
         total_duration=Sum('duration'),
         activity_count=Count('id')
     )
     
    chart_day = create_activities_by_type_chart(request.user, 'day')
    form = ActivityForm()
    context = {
        'today_activities': today_activities,
        'tag_stats': tag_stats,
        'day_activities_by_type_chart': chart_day,
        'form': form,
     }
    
    return render(request, 'activity_tracker/dashboard_day.html', context)
    
    
@login_required
def dashboard_week_view(request):
    today = timezone.now().date()
    this_week = today - timezone.timedelta(days=today.weekday())
    today_activities = Activity.objects.filter(
        user=request.user, 
        start_time__date__gte=this_week
    ).order_by('-start_time')
    
    tag_stats = Activity.objects.filter(
        user=request.user, 
        start_time__date__gte=this_week
    ).values('activity_type') \
     .annotate(
         total_duration=Sum('duration'),
         activity_count=Count('id')
     )
    chart_week = create_activities_by_type_chart(request.user, 'week')
    form = ActivityForm()
    context = {
        'today_activities': today_activities,
        'tag_stats': tag_stats,
        'week_activities_by_type_chart': chart_week,
        'form': form,
     }
    
    return render(request, 'activity_tracker/dashboard_week.html', context)


@login_required
def dashboard_month_view(request):
    this_month = timezone.now().replace(day=1).date()
    today = timezone.now().date()
    today_activities = Activity.objects.filter(
        user=request.user, 
        start_time__date__gte=this_month
    ).order_by('-start_time')
    
    tag_stats = Activity.objects.filter(
        user=request.user, 
        start_time__date__gte=this_month
    ).values('activity_type') \
     .annotate(
         total_duration=Sum('duration'),
         activity_count=Count('id')
     )
    
    chart_month = create_activities_by_type_chart(request.user, 'month')
    form = ActivityForm()
    context = {
        'today_activities': today_activities,
        'tag_stats': tag_stats,
        'month_activities_by_type_chart': chart_month,
        'form': form,
     }
    
    return render(request, 'activity_tracker/dashboard_month.html', context)
    
    
     
    
    