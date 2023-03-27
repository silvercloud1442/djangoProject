from django.core.exceptions import ValidationError

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        return context

def min_valid(value):
    if value < 0:
        raise ValidationError('Неккоректный ввод')