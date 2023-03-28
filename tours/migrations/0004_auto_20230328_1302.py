# Generated by Django 3.2.18 on 2023-03-28 10:02

from django.db import migrations, models
import tours.models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_alter_tours_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['tour'], 'verbose_name': 'Заказ тура', 'verbose_name_plural': 'Заказы туров'},
        ),
        migrations.AlterModelOptions(
            name='clients',
            options={'ordering': ['login'], 'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='hotelimages',
            options={'ordering': ['hotel'], 'verbose_name': 'Фото отеля', 'verbose_name_plural': 'Фото отелей'},
        ),
        migrations.AlterModelOptions(
            name='hotels',
            options={'ordering': ['name'], 'verbose_name': 'Отель', 'verbose_name_plural': 'Отели'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['client'], 'verbose_name': 'Платежная информация', 'verbose_name_plural': 'Платежная информация'},
        ),
        migrations.AlterModelOptions(
            name='rooms',
            options={'ordering': ['hotel'], 'verbose_name': 'Комната в отеле', 'verbose_name_plural': 'Комнаты в отелях'},
        ),
        migrations.AlterModelOptions(
            name='tourimages',
            options={'ordering': ['tour'], 'verbose_name': 'Фото тура', 'verbose_name_plural': 'Фото туров'},
        ),
        migrations.AlterModelOptions(
            name='tours',
            options={'ordering': ['name'], 'verbose_name': 'Тур', 'verbose_name_plural': 'Туры'},
        ),
        migrations.AddField(
            model_name='hotels',
            name='main_image',
            field=models.ImageField(blank=True, upload_to=tours.models.hotel_main_photo_location, verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='main_image',
            field=models.ImageField(blank=True, upload_to=tours.models.hotel_photo_location, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='hotelimages',
            name='image',
            field=models.ImageField(upload_to=tours.models.hotel_photo_location, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='tourimages',
            name='image',
            field=models.ImageField(upload_to=tours.models.tour_photo_location, verbose_name='Изображение'),
        ),
    ]
