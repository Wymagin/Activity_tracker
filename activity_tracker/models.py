from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.timezone import now

class Activity(models.Model):
    TAGS = [
        ('work', 'Work'),
        ('hobby', 'Hobby'),
        ('exercise', 'Exercise'),
        ('personal', 'Personal'),
        ('shopping', 'Shopping'),
        ('learning', 'Learning'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    activity_type = models.CharField(
        max_length=20, 
        choices=TAGS, 
        default='other'
    )
    
    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()  # Call parent clean() if necessary

        # Ensure end_time is after start_time
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after the start time.")

        # Example of enforcing duration validity
        if self.duration is not None and self.duration.total_seconds() < 0:
            raise ValidationError("Duration cannot be negative.")

    def save(self, *args, **kwargs):
        # Validate the input 
        self.clean()
        # Auto-calculate duration if not provided
        if self.start_time and self.end_time and not self.duration:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)
        
    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['activity_type']),
        ]
        
        
class Expense(models.Model):
    TAGS = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills'),
        ('shopping', 'Shopping'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=TAGS, default='other')
    date = models.DateField(default=datetime.now)
    description = models.TextField(blank=True)
    activity = models.ForeignKey('Activity', on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='expenses')
    
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    week = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
    
    def clean(self):
        super().clean()  # Call parent clean() if necessary
        # Ensure amount is positive
        if self.amount <= 0:
            raise ValidationError("Amount must be positive.")
        
    def save(self, *args, **kwargs):
        if self.date:
            self.year = self.date.year
            self.month = self.date.month
            self.week = self.date.isocalendar()[1]
        # Validate the input 
        self.clean()
        super().save(*args, **kwargs)
        
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date']),
            models.Index(fields=['category']),
            models.Index(fields=['year']),
            models.Index(fields=['month']),
            models.Index(fields=['activity']),
        ]