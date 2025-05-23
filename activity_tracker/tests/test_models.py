import pytest
from activity_tracker.models import Activity, User, Expense      
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import models


# Activity model tests

@pytest.mark.django_db
def test_activity_creation():
    user = User.objects.create(username="testuser")
    activity = Activity.objects.create(
        user=user,
        activity_type="work",
        name="Test Activity",
        description="This is a test activity",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        end_time=datetime(2023, 10, 1, 11, 0, 0),

    )

    assert activity.user == user
    assert activity.activity_type == "work"
    assert activity.name == "Test Activity"
    assert activity.description == "This is a test activity"
    assert activity.start_time == datetime(2023, 10, 1, 10, 0, 0)
    assert activity.end_time == datetime(2023, 10, 1, 11, 0, 0)
    assert activity.duration == datetime(2023, 10, 1, 11, 0, 0) - datetime(2023, 10, 1, 10, 0, 0)
    assert activity.duration.total_seconds() == 3600
    
    
@pytest.mark.django_db
def test_activity_creation_invalid_end_time_raises_validation_error():
    user = User.objects.create(username="testuser")
    activity = Activity(
        user=user,
        activity_type="work",
        name="Test Activity",
        description="This is a test activity",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        end_time=datetime(2023, 10, 1, 9, 0, 0),  # Invalid end time
    )
    with pytest.raises(ValidationError, match="End time must be after the start time."):
        activity.full_clean()

@pytest.mark.django_db
def test_activity_creation_negative_duration_raises_validation_error():
    user = User.objects.create(username="testuser")
    activity = Activity(
        user=user,
        activity_type="work",
        name="Test Activity",
        description="This is a test activity",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        duration=timedelta(hours=-1),  # Negative duration
    )
    with pytest.raises(ValidationError, match="Duration cannot be negative."):
        activity.full_clean()
        
@pytest.mark.django_db
def test_activity_creation_with_duration():
    user = User.objects.create(username="testuser")
    activity = Activity.objects.create(
        user=user,
        activity_type="work",
        name="Test Activity",
        description="This is a test activity",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        duration=timedelta(hours=1),  # Duration provided
    )

    assert activity.duration == timedelta(hours=1)
    assert activity.end_time is None
    assert activity.start_time == datetime(2023, 10, 1, 10, 0, 0)

# Expense model tests

@pytest.mark.django_db
def test_expense_creation():
    user = User.objects.create(username="testuser")
    
    expense = Expense.objects.create(
        user=user,
        amount=100.00,
        category='food',
        date=datetime(2023, 10, 1),
        description="Test Expense",
    )

    assert expense.user == user
    assert expense.amount == 100.00
    assert expense.category == 'food'
    assert expense.date == datetime(2023, 10, 1)
    assert expense.description == "Test Expense"
    
@pytest.mark.django_db
def test_expense_year_month_week_auto_populate():
    user = User.objects.create(username="testuser")
    
    expense = Expense.objects.create(
        user=user,
        amount=100.00,
        category='food',
        date=datetime(2023, 10, 1),
        description="Test Expense",
    )

    assert expense.year == 2023
    assert expense.month == 10
    assert expense.week == 39
    
@pytest.mark.django_db
def test_expense_creation_negative_amount_raises_validation_error():
    user = User.objects.create(username="testuser")
    
    expense = Expense(
        user=user,
        amount=-100.00,  # Negative amount
        category='food',
        date=datetime(2023, 10, 1),
        description="Test Expense",
    )
    with pytest.raises(ValidationError, match="Amount must be positive."):
        expense.full_clean()

@pytest.mark.django_db
def test_expense_creation_with_activity():
    user = User.objects.create(username="testuser")
    activity = Activity.objects.create(
        user=user,
        activity_type="work",
        name="Test Activity",
        description="This is a test activity",
        start_time=datetime(2023, 10, 1, 10, 0, 0),
        end_time=datetime(2023, 10, 1, 11, 0, 0),
    )
    
    expense = Expense.objects.create(
        user=user,
        amount=100.00,
        category='food',
        date=datetime(2023, 10, 1),
        description="Test Expense",
        activity=activity,
    )

    assert expense.category == 'food'
    assert expense.date == datetime(2023, 10, 1)
    assert expense.description == "Test Expense"
    assert expense.date == datetime(2023, 10, 1)
    assert expense.activity == activity
    assert expense.activity.user == user
    assert expense.activity.name == "Test Activity"
    assert expense.activity.activity_type == "work"
    assert expense.activity.description == "This is a test activity"
    assert expense.activity.start_time == datetime(2023, 10, 1, 10, 0, 0)

# Class Expense(models.Model):
#     TAGS = [
#         ('food', 'Food'),
#         ('transport', 'Transport'),
#         ('entertainment', 'Entertainment'),
#         ('bills', 'Bills'),
#         ('shopping', 'Shopping'),
#         ('other', 'Other')
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.CharField(max_length=20, choices=TAGS, default='other')
#     date = models.DateField(default=datetime.now)
#     description = models.TextField(blank=True)
#     activity = models.ForeignKey('Activity', on_delete=models.SET_NULL, null=True, blank=True, 
#                                 related_name='expenses')
    
#     year = models.IntegerField(null=True, blank=True)
#     month = models.IntegerField(null=True, blank=True)
#     week = models.IntegerField(null=True, blank=True)

# activity_tracker/models.py
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField(null=True, blank=True)
#     duration = models.DurationField(null=True, blank=True)
    
#     activity_type = models.CharField(
#         max_length=20, 
#         choices=TAGS, 
#         default='other'