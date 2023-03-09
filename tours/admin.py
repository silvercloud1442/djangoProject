from django.contrib import admin
from tours.models import *

class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'image', 'category')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tour, TourAdmin)
