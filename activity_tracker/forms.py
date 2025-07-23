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
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'  # <-- critical
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'  # <-- critical
            ),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activity_type': forms.Select(attrs={'class': 'form-select'}),
        }

class ExpenseInlineForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be positive.")
        return amount

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description', 'activity']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
    