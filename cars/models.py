# D:\mycar\cars\models.py
from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    year = models.IntegerField()
    seats = models.IntegerField(help_text="Number of seats in the car")
    location = models.CharField(max_length=200, help_text="Where the car is located")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    main_image = models.ImageField(upload_to='cars/')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.name}"

    class Meta:
        app_label = 'cars'

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/')
    
    def __str__(self):
        return f"Image for {self.car.name}"

    class Meta:
        app_label = 'cars'

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.car.name}"

    class Meta:
        app_label = 'cars'

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment")
    cardholder_name = models.CharField(max_length=100)
    card_last4 = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for booking #{self.booking.id}"

    class Meta:
        app_label = 'cars'

class Review(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.comment[:20]}"

    class Meta:
        app_label = 'cars'