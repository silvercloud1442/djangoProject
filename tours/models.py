from django.db import models
from django.core.exceptions import ValidationError
from tours.utils import min_valid
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

class Hotels(models.Model):
    name = models.TextField(max_length=255, verbose_name='Название')
    slug = models.SlugField(name, max_length=255)
    description = models.TextField(verbose_name='Описание')
    contact_info = models.CharField(max_length=100, verbose_name='Контактная информация')
    city = models.CharField(max_length=50, verbose_name='Город')
    rating = models.FloatField(verbose_name='Рейтинг')
    food = models.CharField(max_length=50, verbose_name='Питание')

    def clean(self):
        cleaned_data = super(Hotels, self).clean()
        rt = cleaned_data.get('rating')
        if rt:
            if rt < 0:
                raise ValidationError('Некорректный рейтинг')
        return cleaned_data

class Rooms(models.Model):
    description = models.TextField(verbose_name='')
    add_price = models.IntegerField(validators=[min_valid], verbose_name='')
    solo_places = models.IntegerField(validators=[min_valid], verbose_name='')
    twin_places = models.IntegerField(validators=[min_valid], verbose_name='')
    count_in_hotel = models.IntegerField(validators=[min_valid], verbose_name='')
    hotel = models.ForeignKey(to=Hotels, on_delete=models.CASCADE)

class Tours(models.Model):
    name = models.CharField(max_length=255, verbose_name='')
    description = models.TextField(verbose_name='')
    city = models.CharField(max_length=255, verbose_name='')
    duration_days = models.IntegerField(verbose_name='')
    max_adults = models.IntegerField(validators=[min_valid], verbose_name='')
    max_kids = models.IntegerField(validators=[min_valid], verbose_name='')
    base_price = models.IntegerField(validators=[min_valid], verbose_name='')
    need_inter_pass = models.BooleanField(verbose_name='')
    transit_in = models.OneToOneField(Transit, on_delete=models.PROTECT, related_name='transit_in_relate')
    transit_back = models.OneToOneField(Transit, on_delete=models.PROTECT, related_name='transit_back_relate')
    hotel = models.ForeignKey(to=Hotels, on_delete=models.PROTECT)
    room = models.ForeignKey(to=Rooms, on_delete=models.PROTECT)

    def clean(self):
        cleaned_data = super(Tours, self).clean()
        ad = cleaned_data.get('max_adults')
        ki = cleaned_data.get('max_kids')
        if ad + ki == 0:
            raise ValidationError('Некорректное количество клиентов')
        return cleaned_data

class Clients(models.Model):
    login = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=50, verbose_name='Пароль')
    FIO = models.CharField(max_length=255, verbose_name='ФИО')
    birthday = models.DateField(verbose_name='Дата рождения', blank=True)
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True)
    passport_series_number = models.CharField(max_length=30, verbose_name='Серия и номер паспорта', unique=True)
    inter_passport_series_number = models.CharField(max_length=30, verbose_name='Серия и номер загранпаспорта', unique=True, blank=True)
    inter_passport_date = models.DateField(verbose_name='Дата загранпаспорта')

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
    client = models.ForeignKey(to=Clients, on_delete=models.CASCADE)

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

class Booking(models.Model):
    payment_status = models.CharField(max_length=255, verbose_name='')
    adults_count = models.IntegerField(validators=[min_valid], verbose_name='')
    kids_count = models.IntegerField(validators=[min_valid], verbose_name='')
    total_price = models.IntegerField(verbose_name='')
    tour = models.ForeignKey(to=Tours, on_delete=models.PROTECT)
    client = models.ForeignKey(to=Clients, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        tour_price = self.tour.base_price
        rooms_price = self.tour.room.add_price
        self.total_price = tour_price + rooms_price
        self.tour.save()
        self.tour.room.save()
        super(Booking, self).save(*args, **kwargs)

class HotelImages(models.Model):
    image = models.ImageField()