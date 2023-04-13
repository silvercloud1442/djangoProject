from django.contrib import admin
from django.forms import Textarea, TextInput
from django.utils.safestring import mark_safe
from tours.models import *


class TransitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'transit_id', 'start_place', 'end_place', 'start_datetime', 'end_datetime')
    list_display_links = ('pk', 'transit_id',)
    fields = ('transit_id', 'start_place', 'end_place', 'start_datetime', 'end_datetime')
    save_on_top = True

class HotelsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'contact_info', 'city', 'rating', 'food', 'get_html_image')
    list_display_links = ('pk', 'name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}
    fields = ('name', 'slug', 'description', 'contact_info', 'city', 'rating', 'food', 'main_image')
    save_on_top = True

    def get_html_image(self, object):
        if object.main_image:
            return mark_safe(f"<img src='{object.main_image.url}', width=50>")

class RoomsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description', 'add_price', 'solo_places', 'twin_places', 'hotel', 'get_html_image')
    list_display_links = ('pk', 'description',)
    fields = ('description', 'add_price', 'solo_places', 'twin_places', 'hotel', 'main_image')
    save_on_top = True

    def get_html_image(self, object):
        if object.main_image:
            return mark_safe(f"<img src='{object.main_image.url}', width=50>")

class ToursAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'short_description', 'city', 'duration_days', 'max_adults', 'max_kids', 'base_price', 'need_inter_pass', 'transit_in', 'transit_back', 'hotel', 'get_html_image')
    list_display_links = ('pk', 'name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}
    fields = ('name', 'slug', 'description', 'city', 'duration_days', 'max_adults', 'max_kids', 'base_price', 'need_inter_pass', 'transit_in', 'transit_back', 'hotel', 'main_image')
    save_on_top = True

    def get_html_image(self, object):
        if object.main_image:
            return mark_safe(f"<img src='{object.main_image.url}', width=50>")

    def short_description(self, object):
        if object.description:
            return object.description[:35] + '...'

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'FIO', 'birthday', 'email', 'phone', 'passport_series_number', 'inter_passport_series_number',)
    list_display_links = ('pk', 'FIO',)
    search_fields = ('FIO',)
    fields = ('user', 'FIO', 'birthday', 'email', 'phone', 'passport_series_number', 'inter_passport_series_number',)
    save_on_top = True

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'payment_system', 'card_number', 'card_date', 'client')
    list_display_links = ('pk', 'card_number', )
    search_fields = ('card_number',)
    fields = ('payment_system', 'card_number', 'card_date', 'client')
    save_on_top = True

class BookingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'payment', 'adults_count', 'kids_count', 'total_price', 'tour', 'client', 'room')
    list_display_links = ('pk', 'payment',)
    readonly_fields = ('total_price',)
    save_on_top = True

class HotelImagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'hotel', 'get_html_image')
    list_display_links = ('pk', 'hotel',)
    readonly_fields = ('get_html_image',)
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}', width=50>")

    get_html_image.short_description = 'Изображение'

class TourImagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tour', 'get_html_image')
    list_display_links = ('pk', 'tour',)
    readonly_fields = ('get_html_image',)
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}', width=50>")

    get_html_image.short_description = 'Изображение'

admin.site.register(Transit, TransitAdmin)
admin.site.register(Hotels, HotelsAdmin)
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Tours, ToursAdmin)
admin.site.register(Clients, ClientsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(HotelImages, HotelImagesAdmin)
admin.site.register(TourImages, TourImagesAdmin)

admin.site.site_header = 'Кто админ-?=|!@#$%^&*()_+\,/ Тот чёрт!'

