from django.shortcuts import render


def base_view(request):
    return render(request, 'activity_tracker/base.html', {
        'title': 'Activity Tracker',
        'welcome_message': 'Track and Manage Your Activities',
    })
    
def home_view(request):
    return render(request, 'activity_tracker/home.html')