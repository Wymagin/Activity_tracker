from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Activity, Expense


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ActivityForm(forms.ModelForm):
    add_expense = forms.BooleanField(
        required=False, 
        label="Add a related expense?"
    )
    class Meta:
        model = Activity
        fields = ['name', 'description', 'start_time', 'end_time', 'activity_type']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activity_type': forms.Select(attrs={'class': 'form-select'}),
        }

class ExpenseInlineForm(forms.ModelForm):
    class Meta:
        model = Expense
        # We don't need 'activity' or 'user' here. The view and formset will handle them.
        fields = ['amount', 'category', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description', 'activity']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
    