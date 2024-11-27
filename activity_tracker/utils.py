import plotly.express as px
import plotly.offline as opy
import pandas as pd
from django.db.models import Count, Sum, DurationField
from django.db.models.functions import TruncDate
from .models import Activity


def aggregate_daily_activities(user):
    daily_activities = Activity.objects.filter(user=user).annotate(
        day=TruncDate('start_time')
    ).values('day').annotate(
        activity_count=Count('id'),
        total_duration=Sum('duration', output_field=DurationField())
    ).order_by('day')
    
    return daily_activities


def create_daily_activities_chart(user):
    daily_activities = aggregate_daily_activities(user)
    
    # Convert to DataFrame
    df = pd.DataFrame(daily_activities)
    
    # Convert duration to minutes for better visualization
    df['total_duration_minutes'] = df['total_duration'].apply(lambda x: x.total_seconds() / 60 if x else 0)
    
    # Create plotly figure
    fig = px.bar(
        df, 
        x='day', 
        y='total_duration_minutes', 
        color='activity_count',
        title='Daily Activity Duration',
        labels={
            'day': 'Date', 
            'total_duration_minutes': 'Total Duration (minutes)',
            'activity_count': 'Number of Activities'
        }
    )
    
    # Convert to div
    chart_div = opy.plot(fig, output_type='div', include_plotlyjs=True)
    return chart_div