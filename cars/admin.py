from django.contrib import admin
from .models import Car, CarImage, Booking, Review

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'year', 'price_per_day', 'available']
    list_filter = ['brand', 'year', 'available']
    search_fields = ['name', 'brand']
    inlines = [CarImageInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'comment']

admin.site.register(Car, CarAdmin)
admin.site.register(Booking)
admin.site.register(Review, ReviewAdmin)
