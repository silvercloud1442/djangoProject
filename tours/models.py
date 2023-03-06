from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

class Tour(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название тура')
    description = models.TextField(verbose_name='Описание тура')
    price = models.IntegerField(verbose_name='Цена')
    image = models.ImageField(upload_to='tours_images', verbose_name='Изображение')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f"Название тура : {self.name} | Описание тура : {self.description}"