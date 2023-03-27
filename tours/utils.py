from django.core.exceptions import ValidationError
from datetime import date

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