from django.db import models
from django.forms import ValidationError
from datetime import date


class Transit(models.Model):
    transit_id = models.CharField(max_length=255, verbose_name='Идентификатор транспорта')
    start_place = models.CharField(max_length=255, verbose_name='Начальная точка')
    end_place = models.CharField(max_length=255, verbose_name='Конечная точка')
    start_datetime = models.DateTimeField(verbose_name='Начальное время')
    end_datetime = models.DateTimeField(verbose_name='Конечное время')

    def clean(self):
        cleande_date = super(Transit, self).clean()
        s_dtm = cleande_date.get('start_datetime')
        e_dtm = cleande_date.get('end_datetime')
        if s_dtm and e_dtm:
            if e_dtm < s_dtm:
                raise ValidationError('Некорректные дата и время')
        return cleande_date

class Hotel(models.Model):
    name = models.TextField(max_length=255, verbose_name='')
    slug = models.SlugField(name, max_length=255, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    contact_info = models.CharField(verbose_name='Контактная информация')
    city = models.CharField(verbose_name='Город')
    rating = models.FloatField(verbose_name='Рейтинг')
    food = models.CharField(verbose_name='Питание')

    def clean(self):
        cleaned_data = super(Hotel, self).clean()
        rt = cleaned_data.get('rating')
        if rt:
            if rt < 0:
                raise ValidationError('Некорректный рейтинг')
        return cleaned_data

class Clients(models.Model):
    login = models.CharField(unique=True, verbose_name='Логин')
    password = models.CharField(verbose_name='')
    FIO = models.CharField(max_length=255, verbose_name='')
    birthday = models.DateField(verbose_name='', blank=True)
    email = models.EmailField(verbose_name='')
    phone = models.CharField(max_length=20, verbose_name='', blank=True)
    passport_series_number = models.CharField(max_length=30, verbose_name='', unique=True)
    inter_passport_series_number = models.CharField(max_length=30, verbose_name='', unique=True, blank=Ture)
    inter_passport_date = models.DateField

    def clean(self):
        cleaned_data = super(Clients, self).clean()
        ipd = cleaned_data.get('inter_passport_date')
        if ipd:
            if ipd < date.today():
                raise ValidationError('Некорректная дата загран. паспорта')
        return cleaned_data

class Payment(models.Model):
    payment_system = models.CharField(max_length=30, verbose_name='')
    card_number = models.CharField(max_length=20, verbose_name='')
    card_date = models.DateField(verbose_name='')
    client_id = models.ForeignKey(to=Clients, on_delete="CASCADE")

    def clean(self):
        cleaned_data = super(Payment, self).clean()
        cn = cleaned_data.get('card_number')
        cd = cleaned_data.get('card_date')

        if cn:
            if len(cn) != 16:
                raise ValidationError('Некорректный номер карты')
        if cd:
            if cd < date.today():
                raise ValidationError('Неккоректная дата')


