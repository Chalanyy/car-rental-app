from django.contrib import admin
from .models import Car, CarImage, Booking

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'year', 'price_per_day', 'available']
    list_filter = ['brand', 'year', 'available']
    search_fields = ['name', 'brand']
    inlines = [CarImageInline]

admin.site.register(Car, CarAdmin)
admin.site.register(Booking)