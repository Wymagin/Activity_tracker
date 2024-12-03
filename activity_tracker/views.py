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

def base_view(request):
    return render(request, 'activity_tracker/base.html', {
        'title': 'Activity Tracker',
        'welcome_message': 'Track and Manage Your Activities',
    })
    
def home_view(request):
    return render(request, 'activity_tracker/home.html')


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
        return reverse_lazy('home')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    # Get today's activities
    today = timezone.now().date()
    today_activities = Activity.objects.filter(
        user=request.user, 
        start_time__date=today
    ).order_by('-start_time')
    
    # Tag-based statistics
    tag_stats = Activity.objects.filter(
        user=request.user, 
        start_time__date=today
    ).values('activity_type') \
     .annotate(
         total_duration=Sum('duration'),
         activity_count=Count('id')
     )

    daily_activities_chart = create_daily_activities_chart(request.user)
    activities_by_type_chart = create_activities_by_type_chart(request.user)
    form = ActivityForm()
    
    context = {
        'today_activities': today_activities,
        'tag_stats': tag_stats,
        'daily_activities_chart': daily_activities_chart,
        'activities_by_type_chart': activities_by_type_chart,
        'form': form,
    }
    
    return render(request, 'activity_tracker/dashboard.html', context)


# @login_required
# def add_activity(request):
#     if request.method == 'POST':
#         form = ActivityForm(request.POST)
#         if form.is_valid():
#             activity = form.save(commit=False)
#             activity.user = request.user  
#             activity.save()
#             messages.success(request, "Activity added successfully!")
#             return redirect('dashboard') 
#         else:
#             messages.error(request, "There was an error in your form. Please fix it and try again.")
#     else:
#         form = ActivityForm()

#     return render(request, 'activity_tracker/add_activity.html', {'form': form})

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
