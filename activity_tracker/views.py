from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, ActivityForm
from .models import Activity
from django.contrib import messages


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