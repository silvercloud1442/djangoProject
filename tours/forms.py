from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from tours.models import *

class AddTourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Не выбрано'

    class Meta:
        model = Tour
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'input-group-text'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 5})
        }

    def clead_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class" : 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class" : 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={"class" : 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class" : 'form-control'}))

class ContactForm(forms.Form):
    name = forms.CharField(label='name', max_length=255)
    email = forms.EmailField(label='email')
    context = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()