from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tour(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название тура')
    description = models.TextField(verbose_name='Описание тура')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='tours_images', verbose_name='Изображение')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_tour', kwargs={'tour_id': self.pk})

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
