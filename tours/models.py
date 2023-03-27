from django.db import models
from tours.utils import *

class Transit(models.Model):
    transit_id = models.CharField(max_length=255, verbose_name='Идентификатор транспорта')
    start_place = models.CharField(max_length=255, verbose_name='Начальная точка')
    end_place = models.CharField(max_length=255, verbose_name='Конечная точка')
    start_datetime = models.DateTimeField(verbose_name='Начальное время')
    end_datetime = models.DateTimeField(verbose_name='Конечное время')

    # def clean(self):
    #     cleande_date = super(Transit, self).clean()
    #     s_dtm = cleande_date.get('start_datetime')
    #     e_dtm = cleande_date.get('end_datetime')
    #     if s_dtm and e_dtm:
    #         if e_dtm < s_dtm:
    #             raise ValidationError('Некорректные дата и время')
    #     return cleande_date

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

class Rooms(models.Model):
    description = models.TextField(verbose_name='Описание')
    add_price = models.IntegerField(validators=[min_valid], verbose_name='Добавочная стоимость')
    solo_places = models.IntegerField(validators=[min_valid], verbose_name='одиночных мест')
    twin_places = models.IntegerField(validators=[min_valid], verbose_name='Двойных мест')
    total_places = models.IntegerField(verbose_name='Всего мест')
    hotel = models.ForeignKey(to=Hotels, on_delete=models.CASCADE, verbose_name='Отель')

    def save(self, *args, **kwargs):
        self.total_places = self.solo_places + (self.twin_places * 2)
        super(Rooms, self).save(*args, **kwargs)

    # def __str__(self):
    #     return f"Всего мест {self.total_places}" \
    #            f"Односпальных : {self.solo_places}"\
    #            f"Двуспальных : {self.twin_places}"

    class Meta:
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
    hotel = models.ForeignKey(to=Hotels, on_delete=models.PROTECT, verbose_name='Отель')

    # def clean(self):
    #     cleaned_data = super(Tours, self).clean()
    #     ad = cleaned_data.get('max_adults')
    #     ki = cleaned_data.get('max_kids')
    #     if ad + ki == 0:
    #         raise ValidationError('Некорректное количество клиентов')
    #     return cleaned_data

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

class Clients(models.Model):
    login = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=50, verbose_name='Пароль')
    FIO = models.CharField(max_length=255, verbose_name='ФИО')
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True)
    passport_series_number = models.CharField(max_length=30, verbose_name='Серия и номер паспорта', unique=True)
    inter_passport_series_number = models.CharField(max_length=30, verbose_name='Серия и номер загранпаспорта', unique=True, blank=True)
    inter_passport_date = models.DateField(verbose_name='Дата загранпаспорта', blank=True, null=True)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     ipd = cleaned_data.get('inter_passport_date')
    #     if ipd:
    #         if ipd < date.today():
    #             raise ValidationError('Некорректная дата загран. паспорта')
    #     return cleaned_data

    def __str__(self):
        return self.FIO

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class Payment(models.Model):
    payment_system = models.CharField(max_length=30, verbose_name='Система оплаты')
    card_number = models.CharField(validators=[car_number_valid], max_length=20, verbose_name='Номер карта')
    card_date = models.DateField(validators=[date_valid], verbose_name='Срок карты')
    client = models.ForeignKey(to=Clients, on_delete=models.CASCADE, verbose_name='Клиент')

    # def clean(self):
    #     cleaned_data = super(Payment, self).clean()
    #     cn = cleaned_data.get('card_number')
    #     cd = cleaned_data.get('card_date')
    #
    #     if cn:
    #         if len(cn) != 16:
    #             raise ValidationError('Некорректный номер карты')
    #     if cd:
    #         if cd < date.today():
    #             raise ValidationError('Неккоректная дата')

    class Meta:
        verbose_name = 'Платежная информация'
        verbose_name_plural = 'Платежная информация'

class Booking(models.Model):
    payment_status = models.CharField(max_length=255, verbose_name='Статус опалты')
    adults_count = models.IntegerField(validators=[min_valid], verbose_name='Всего взрослых')
    kids_count = models.IntegerField(validators=[min_valid], verbose_name='Всего детей')
    total_price = models.IntegerField(verbose_name='Общая стоимость')
    tour = models.ForeignKey(to=Tours, on_delete=models.PROTECT, verbose_name='Тур')
    client = models.ForeignKey(to=Clients, on_delete=models.PROTECT, verbose_name='Клиент')
    room = models.ForeignKey(to=Rooms, on_delete=models.PROTECT, verbose_name='Комната')

    def save(self, *args, **kwargs):
        tour_price = self.tour.base_price
        rooms_price = self.room.add_price
        self.total_price = tour_price + rooms_price
        self.tour.save()
        super(Booking, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ тура'
        verbose_name_plural = 'Заказы туров'

def hotel_photo_location(self, filename):
    return 'hotels/{}/{}'.format(self.hotel.slug, filename)

class HotelImages(models.Model):
    hotel = models.ForeignKey(to=Hotels, verbose_name='Отель', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hotel_photo_location, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        hslug = self.hotel.slug
        self.image.upload_to = f'hotels_images/{hslug}'
        self.hotel.save()
        super(HotelImages, self).save()

    class Meta:
        verbose_name = 'Фото отеля'
        verbose_name_plural = 'Фото отелей'

def tour_photo_location(self, filename):
    return 'tours/{}/{}'.format(self.tour.slug, filename)

class TourImages(models.Model):
    tour = models.ForeignKey(to=Tours, on_delete=models.CASCADE, verbose_name='Тур')
    image = models.ImageField(upload_to=tour_photo_location, verbose_name='Изображение')



    def save(self, *args, **kwargs):
        tslug = self.tour.slug
        self.image.upload_to = f'tours_images/{tslug}'
        self.tour.save()
        super(TourImages, self).save()

    class Meta:
        verbose_name = 'Фото тура'
        verbose_name_plural = 'Фото туров'