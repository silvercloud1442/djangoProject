from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from tours.models import Clients

class DateInput(forms.DateInput):
    input_type = "date"

class PasswordInput(forms.PasswordInput):
    input_type = "password"

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='*Login')
    password1 = forms.CharField(label='*Password', widget=PasswordInput)
    password2 = forms.CharField(label='*Confirm password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class RegisterClientForm(forms.ModelForm):
    FIO = forms.CharField(label='*FIO')
    birthday = forms.DateField(label='*Birthday', widget=DateInput)
    email = forms.EmailField(label='*Email')
    phone = forms.CharField(label="phone", required=False)
    passport_series_number = forms.CharField(label='*passport series/number')
    inter_passport_series_number = forms.CharField(label='international passport series/number', required=False)

    class Meta:
        model = Clients
        fields = ('FIO', 'birthday', 'email', 'phone', 'passport_series_number', 'inter_passport_series_number',)
