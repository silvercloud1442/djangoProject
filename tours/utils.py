from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
from django import forms
from django.urls import reverse_lazy, reverse




class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        return context


def min_valid(value):
    if value:
        if value < 0:
            raise ValidationError('Неккоректный ввод')

def date_valid(date_in):
    if date_in:
        td = date.today()
        if date_in < td:
            raise  ValidationError('Некорректная дата')

def car_number_valid(number):
    if len(number) != 16:
        raise ValidationError('Некорректный номер карты')