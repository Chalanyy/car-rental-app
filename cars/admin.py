from django.contrib import admin
from cars.models import Car, CarImage, Booking, Review

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'year', 'price_per_day', 'seats', 'location', 'available']
    list_filter = ['brand', 'year', 'available', 'seats', 'location']
    search_fields = ['name', 'brand', 'location']
    inlines = [CarImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'year', 'description')
        }),
        ('Pricing & Availability', {
            'fields': ('price_per_day', 'available')
        }),
        ('Car Details', {
            'fields': ('seats', 'location')
        }),
        ('Images', {
            'fields': ('main_image',)
        }),
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'comment']

admin.site.register(Car, CarAdmin)
admin.site.register(Booking)
admin.site.register(Review, ReviewAdmin)
