from django import forms
from django.core.exceptions import ValidationError

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