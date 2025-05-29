from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import ScheduledMessage

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput())

class SimpleScheduleForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        }),
        label='Message'
    )
    scheduled_time = forms.DateTimeField(
        label='Scheduled Time',
        input_formats=[
            '%Y-%m-%dT%H:%M',     # без секунд
            '%Y-%m-%dT%H:%M:%S',  # с секундами
        ],
        widget=forms.DateTimeInput(
            attrs={'type':'datetime-local','class':'form-control'}
        )
    )

    def clean_scheduled_time(self):
        dt = self.cleaned_data['scheduled_time']
        if dt <= timezone.now():
            raise ValidationError('Please choose a date and time in the future.')
        return dt