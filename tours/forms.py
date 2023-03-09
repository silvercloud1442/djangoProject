from django import forms
from tours.models import *

class AddTourForm(forms.Form):
    name = forms.CharField(max_length=128, label='Название')
    slug = forms.SlugField(max_length=255, label='URL')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Описание')
    price = forms.IntegerField(label='Цена')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Не выбрано')