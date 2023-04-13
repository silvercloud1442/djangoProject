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
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class UppercaseValidator(object):

    '''The password must contain at least 1 uppercase letter, A-Z.'''

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Пароль слишком простой"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Пароль должен содержать заглавные буквы"
        )

def min_valid(value):
    if value:
        if value < 0:
            raise ValidationError('Неккоректный ввод')

def date_valid_revers(date_in):
    if date_in:
        td = date.today()
        if date_in < td:
            raise ValidationError('Некорректная дата')

def date_valid(date_in):
    if date_in:
        td = date.today()
        if date_in < td:
            raise ValidationError('Некорректная дата')

def car_number_valid(number):
    if len(number) != 16:
        raise ValidationError('Некорректный номер карты')