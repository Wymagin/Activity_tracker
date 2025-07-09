from datetime import timedelta
from django.utils import timezone
import plotly.express as px
import plotly.offline as opy
import pandas as pd
from django.db.models import Count, Sum, DurationField
from django.db.models.functions import TruncDate, TruncDay, TruncWeek, TruncMonth, TruncYear
from .models import Activity, Expense
from .forms import ActivityForm, ExpenseInlineForm

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



def agg_expenses_by_category(user):
    expenses = Expense.objects.filter(user=user)
    return expenses.values('category').annotate(total_amount=Sum('amount'))


def create_expenses_tree_chart(user):
    data = pd.DataFrame(agg_expenses_by_category(user))
    if data.empty:
        # Provide a placeholder row if there are no expenses
        data = pd.DataFrame([{"category": "No data", "total_amount": 0}])
        
    fig = px.treemap(
        data,
        path=["category"],
        values="total_amount",
        title="Your Spending Breakdown by Category"
    )
    fig.update_layout(
        margin=dict(t=40, l=0, r=0, b=0),
    )
    fig.update_traces(
        textinfo="label+value+percent entry",
        textfont=dict(size=15),
        hovertemplate="<b>%{label}</b><br>Amount: %{value}<br>Percent: %{percentEntry:.2%}<extra></extra>"
    )
    return opy.plot(fig, output_type='div', include_plotlyjs=True)


# Todo
# chart_day = create_activities_by_type_chart(user, 'day')
# chart_week = create_activities_by_type_chart(user, 'week')
# chart_month = create_activities_by_type_chart(user, 'month')


def create_demo_bar_chart():
    data = {
            'day': [(timezone.now().date() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)],
            'total_duration': [
                timedelta(hours=1.5),
                timedelta(hours=2),
                timedelta(hours=1),
                timedelta(hours=3),
                timedelta(hours=2.5),
                timedelta(hours=1.75),
                timedelta(hours=2.25)
            ],
            'activity_count': [1, 2, 1, 3, 2, 5, 2]
        }
    df = pd.DataFrame(data)
    df['total_duration_hours'] = df['total_duration'].apply(lambda x: x.total_seconds() / 3600)

    fig = px.bar(
        df,
        x='day',
        y='total_duration_hours',
        color='activity_count',
        title='Your weekly Activities',
        labels={
            'day': 'Date', 
            'total_duration_hours': 'Total Duration (hours)',
            'activity_count': 'Number of Activities'
        }
    )
    return opy.plot(fig, output_type='div', include_plotlyjs=True)



def create_demo_pie_chart():
    data = {
            'activity_type': ['Running', 'Cycling', 'Swimming', 'Yoga'],
            'activity_count': [10, 5, 8, 12]
        }
    df = pd.DataFrame(data)
    
    fig = px.pie(df,
                values='activity_count',
                names='activity_type',
                title=f'Your activities by Type',
                labels={'activity_type': 'Activity Type', 'activity_count': 'Number of Activities'},)
    fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    ) 

    return opy.plot(fig, output_type='div', include_plotlyjs=True)


def create_demo_tree_chart():
    data = pd.DataFrame({
        "Category": ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"],
        "Amount": [250, 120, 90, 180, 130, 60]
    })

    fig = px.treemap(
        data,
        path=["Category"],
        values="Amount",
        title="Your Spending Breakdown by Category"
    )
    fig.update_layout(
        margin=dict(t=40, l=0, r=0, b=0),
    )
    fig.update_traces(
        textinfo="label+value+percent entry",
        textfont=dict(size=15),
        hovertemplate="<b>%{label}</b><br>Amount: %{value}<br>Percent: %{percentEntry:.2%}<extra></extra>"
    )

    return opy.plot(fig, output_type='div', include_plotlyjs=True)

def get_dashboard_forms():
    return {
        'activity_form': ActivityForm(),
        'expenses_form': ExpenseInlineForm(),
    }