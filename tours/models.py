from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from django.dispatch import receiver

from tours.utils import *

def hotel_photo_location(self, filename):
    return 'hotels/{}/{}'.format(self.hotel.slug, filename)

def hotel_main_photo_location(self, filename):
    return 'hotels/{}/{}'.format(self.slug, filename)

def tour_photo_location(self, filename):
    return 'tours/{}/{}'.format(self.tour.slug, filename)

def tour_main_photo_location(self, filename):
    return 'tours/{}/{}'.format(self.slug, filename)

class Transit(models.Model):
    transit_id = models.CharField(max_length=255, verbose_name='Идентификатор транспорта')
    start_place = models.CharField(max_length=255, verbose_name='Начальная точка')
    end_place = models.CharField(max_length=255, verbose_name='Конечная точка')
    start_datetime = models.DateTimeField(verbose_name='Начальное время')
    end_datetime = models.DateTimeField(verbose_name='Конечное время')

    def __str__(self):
        return f"({self.start_datetime.date()}) | {self.start_place} - {self.end_place}"

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'

class Hotels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='slug')
    description = models.TextField(verbose_name='Описание')
    contact_info = models.CharField(max_length=100, verbose_name='Контактная информация')
    city = models.CharField(max_length=50, verbose_name='Город')
    rating = models.FloatField(validators=[min_valid], verbose_name='Рейтинг')
    food = models.CharField(max_length=50, verbose_name='Питание')
    main_image = models.ImageField(upload_to=hotel_main_photo_location, verbose_name='Изображение', blank=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 35)

    def get_absolute_url(self):
        return reverse('hotel_details', kwargs={'hotel_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

class Rooms(models.Model):
    description = models.TextField(verbose_name='Описание')
    add_price = models.IntegerField(validators=[min_valid], verbose_name='Добавочная стоимость')
    solo_places = models.IntegerField(validators=[min_valid], verbose_name='одиночных мест')
    twin_places = models.IntegerField(validators=[min_valid], verbose_name='Двойных мест')
    total_places = models.IntegerField(verbose_name='Всего мест')
    hotel = models.ForeignKey(to=Hotels, on_delete=models.CASCADE, verbose_name='Отель')
    main_image = models.ImageField(upload_to=hotel_photo_location, verbose_name='Изображение', blank=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 35)
    def save(self, *args, **kwargs):
        self.total_places = self.solo_places + (self.twin_places * 2)
        super(Rooms, self).save(*args, **kwargs)

    def __str__(self):
        return f'Отель: {self.hotel} | 1x:{self.solo_places} | 2x{self.twin_places}'

    class Meta:
        ordering = ['hotel']
        verbose_name = 'Комната в отеле'
        verbose_name_plural = 'Комнаты в отелях'

class Tours(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='slug')
    description = models.TextField(verbose_name='Описание')
    city = models.CharField(max_length=255, verbose_name='Город/место')
    duration_days = models.IntegerField(verbose_name='длительность (дней)')
    max_adults = models.IntegerField(validators=[min_valid], verbose_name='максимум взрослых')
    max_kids = models.IntegerField(validators=[min_valid], verbose_name='масксимум детей')
    base_price = models.IntegerField(validators=[min_valid], verbose_name='Базовая стоимость')
    need_inter_pass = models.BooleanField(verbose_name='Нужен загранпаспорт')
    transit_in = models.OneToOneField(Transit, on_delete=models.PROTECT, related_name='transit_in_relate', verbose_name='Транспорт туда')
    transit_back = models.OneToOneField(Transit, on_delete=models.PROTECT, related_name='transit_back_relate', verbose_name='Транспорт обратно')
    main_image = models.ImageField(upload_to=tour_main_photo_location, verbose_name='Изображение', blank=True)
    hotel = models.ForeignKey(to=Hotels, on_delete=models.PROTECT, verbose_name='Отель')

    @property
    def short_description(self):
        return truncatechars(self.description, 35)

    def get_absolute_url(self):
        return reverse('tour_details', kwargs={'tour_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

class Clients(models.Model):
    # login = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    # password = models.CharField(max_length=50, verbose_name='Пароль')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FIO = models.CharField(max_length=255, verbose_name='ФИО')
    birthday = models.DateField(verbose_name='Дата рождения', null=True)
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True)
    passport_series_number = models.CharField(max_length=30, verbose_name='Серия и номер паспорта', unique=True)
    inter_passport_series_number = models.CharField(max_length=30, verbose_name='Серия и номер загранпаспорта', blank=True)

    def __str__(self):
        return self.FIO

    class Meta:
        ordering = ['user']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Clients.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.clients.save()

class Payment(models.Model):
    payment_system = models.CharField(max_length=30, verbose_name='Система оплаты')
    card_number = models.CharField(validators=[car_number_valid], max_length=20, verbose_name='Номер карта')
    card_date = models.DateField(validators=[date_valid], verbose_name='Срок карты')
    client = models.ForeignKey(to=Clients, on_delete=models.CASCADE, verbose_name='Клиент')

    def __str__(self):
        return self.payment_system + " : " + self.card_number


    class Meta:
        ordering = ['client']
        verbose_name = 'Платежная информация'
        verbose_name_plural = 'Платежная информация'

class Booking(models.Model):
    payment_status = models.CharField(max_length=255, verbose_name='Статус опалты', blank=True)
    adults_count = models.IntegerField(validators=[min_valid], verbose_name='Всего взрослых')
    kids_count = models.IntegerField(validators=[min_valid], verbose_name='Всего детей')
    total_price = models.IntegerField(verbose_name='Общая стоимость',)
    tour = models.ForeignKey(to=Tours, on_delete=models.PROTECT, verbose_name='Тур')
    client = models.ForeignKey(to=Clients, on_delete=models.PROTECT, verbose_name='Клиент')
    room = models.ForeignKey(to=Rooms, on_delete=models.PROTECT, verbose_name='Комната')

    def save(self, *args, **kwargs):
        tour_price = self.tour.base_price
        rooms_price = self.room.add_price
        self.total_price = tour_price + rooms_price
        self.tour.save()
        super(Booking, self).save(*args, **kwargs)
        self.save()

    class Meta:
        ordering = ['tour']
        verbose_name = 'Заказ тура'
        verbose_name_plural = 'Заказы туров'

class HotelImages(models.Model):
    hotel = models.ForeignKey(to=Hotels, verbose_name='Отель', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hotel_photo_location, verbose_name='Изображение')

    class Meta:
        ordering = ['hotel']
        verbose_name = 'Фото отеля'
        verbose_name_plural = 'Фото отелей'

class TourImages(models.Model):
    tour = models.ForeignKey(to=Tours, on_delete=models.CASCADE, verbose_name='Тур')
    image = models.ImageField(upload_to=tour_photo_location, verbose_name='Изображение')

    class Meta:
        ordering = ['tour']
        verbose_name = 'Фото тура'
        verbose_name_plural = 'Фото туров'