from datetime import timedelta
from django.utils import timezone
import plotly.express as px
import plotly.offline as opy
import pandas as pd
from django.db.models import Count, Sum, DurationField
from django.db.models.functions import TruncDate, TruncDay, TruncWeek, TruncMonth, TruncYear
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
    
    df = pd.DataFrame(daily_activities)
    
    # Convert duration to minutes for better visualization
    df['total_duration_hours'] = df['total_duration'].apply(lambda x: x.total_seconds() / 60 / 60 if x else 0)
    
    # Create plotly figure
    fig = px.bar(
        df, 
        x='day', 
        y='total_duration_hours', 
        color='activity_count',
        title='Daily Activity Duration',
        labels={
            'day': 'Date', 
            'total_duration_hours': 'Total Duration (hours)',
            'activity_count': 'Number of Activities'
        }
    )
    
    # Convert to div
    chart_div = opy.plot(fig, output_type='div', include_plotlyjs=True)
    return chart_div


# def agg_activities_by_type(user, period='year'):
#     now = timezone.now()
#     if period == 'day':
#         start_date = now - timedelta(days=1)
#     elif period == 'week':
#         start_date = now - timedelta(weeks=1)
#     elif period == 'month':
#         start_date = now - timedelta(days=30)
#     elif period == 'year':
#         start_date = now - timedelta(days=365)
#     else:
#         raise ValueError("Invalid period. Choose from 'day', 'week', 'month', or 'year'.")
  
#     activities_by_type = (
#     Activity.objects.filter(user=user, start_time__gte=start_date)
#     .values('activity_type')
#     .annotate(activity_count=Count('id'))
#     .order_by('activity_type')
#     )
#     return activities_by_type

def agg_activities_by_type(user, period):
    now = timezone.now()
    trunc_map = {
        'day': TruncDay('start_time'),
        'week': TruncWeek('start_time'),
        'month': TruncMonth('start_time'),
        'year': TruncYear('start_time')
    }
    
    date_filters = {
        'day': now.date(),
        'week': now.date() - timedelta(days=now.weekday()),
        'month': now.replace(day=1).date(),
        'year': now.replace(month=1, day=1).date()
    }
    
    return (Activity.objects.filter(
            user=user,
            start_time__date__gte=date_filters[period]
        )
        .annotate(period=trunc_map[period])
        .values('activity_type', 'period')
        .annotate(activity_count=Count('id'))
        .order_by('period', 'activity_type'))




def create_activities_by_type_chart(user,period):
    df = pd.DataFrame(agg_activities_by_type(user, period))
    fig = px.pie(df,
                values='activity_count',
                names='activity_type',
                title=f'Activities by Type this {period.title()}',
                labels={'activity_type': 'Activity Type', 'activity_count': 'Number of Activities'},)
    chart_div = opy.plot(fig, output_type='div', include_plotlyjs=True)
    return chart_div


# Todo
# chart_day = create_activities_by_type_chart(user, 'day')
# chart_week = create_activities_by_type_chart(user, 'week')
# chart_month = create_activities_by_type_chart(user, 'month')


def create_demo_chart():
    data = {
            'day': [
                '2025-05-08', '2025-05-09', '2025-05-10',
                '2025-05-11', '2025-05-12', '2025-05-13', '2025-05-14'
            ],
            'total_duration': [
                timedelta(hours=1.5),
                timedelta(hours=2),
                timedelta(hours=1),
                timedelta(hours=3),
                timedelta(hours=2.5),
                timedelta(hours=1.75),
                timedelta(hours=2.25)
            ],
            'activity_count': [1, 2, 1, 3, 2, 2, 2]
        }
    df = pd.DataFrame(data)
    df['total_duration_hours'] = df['total_duration'].apply(lambda x: x.total_seconds() / 3600)

    fig = px.bar(
        df,
        x='day',
        y='total_duration_hours',
        color='activity_count',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title='Sample Daily Activity Chart',
        labels={
            'day': 'Date', 
            'total_duration_hours': 'Total Duration (hours)',
            'activity_count': 'Number of Activities'
        }
        
        
    )
    return opy.plot(fig, output_type='div', include_plotlyjs=True)