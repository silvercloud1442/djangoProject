from django.contrib import admin
from django.utils.safestring import mark_safe

from tours.models import *

class TourAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'get_html_image', 'category')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'description', 'price', 'image', 'get_html_image', 'category')
    readonly_fields = ('get_html_image', )
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")

    get_html_image.short_description = 'Изображение'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tour, TourAdmin)

admin.site.site_header = 'Кто админ, тот чёрт.'
