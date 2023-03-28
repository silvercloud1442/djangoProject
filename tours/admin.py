from django.contrib import admin
from django.forms import Textarea, TextInput
from django.utils.safestring import mark_safe
from tours.models import *


class TransitAdmin(admin.ModelAdmin):
    list_display = ('transit_id', 'start_place', 'end_place', 'start_datetime', 'end_datetime')
    list_display_links = ('transit_id',)
    fields = ('transit_id', 'start_place', 'end_place', 'start_datetime', 'end_datetime')
    save_on_top = True

class HotelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'contact_info', 'city', 'rating', 'food')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}
    fields = ('name', 'slug', 'description', 'contact_info', 'city', 'rating', 'food')
    save_on_top = True

class RoomsAdmin(admin.ModelAdmin):
    list_display = ('description', 'add_price', 'solo_places', 'twin_places', 'hotel')
    list_display_links = ('description',)
    fields = ('description', 'add_price', 'solo_places', 'twin_places', 'hotel')
    save_on_top = True

class ToursAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'city', 'duration_days', 'max_adults', 'max_kids', 'base_price', 'need_inter_pass', 'transit_in', 'transit_back', 'hotel')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', )}
    fields = ('name', 'slug', 'description', 'city', 'duration_days', 'max_adults', 'max_kids', 'base_price', 'need_inter_pass', 'transit_in', 'transit_back', 'hotel')
    save_on_top = True

class ClientsAdmin(admin.ModelAdmin):
    list_display = ('login', 'FIO', 'birthday', 'email', 'phone', 'passport_series_number', 'inter_passport_series_number', 'inter_passport_date')
    list_display_links = ('login', 'FIO')
    search_fields = ('login', 'FIO')
    fields = ('login', 'password', 'FIO', 'birthday', 'email', 'phone', 'passport_series_number', 'inter_passport_series_number', 'inter_passport_date')
    save_on_top = True

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_system', 'card_number', 'card_date', 'client')
    list_display_links = ('card_number', )
    search_fields = ('card_number',)
    fields = ('payment_system', 'card_number', 'card_date', 'client')
    save_on_top = True

class BookingAdmin(admin.ModelAdmin):
    list_display = ('payment_status', 'adults_count', 'kids_count', 'total_price', 'tour', 'client', 'room')
    list_display_links = ('payment_status',)
    readonly_fields = ('total_price',)
    save_on_top = True

class HotelImagesAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'get_html_image')
    list_display_links = ('hotel',)
    readonly_fields = ('get_html_image',)
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}', width=50>")

    get_html_image.short_description = 'Изображение'

class TourImagesAdmin(admin.ModelAdmin):
    list_display = ('tour', 'get_html_image')
    list_display_links = ('tour',)
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

admin.site.site_header = 'Кто админ, тот чёрт!'

