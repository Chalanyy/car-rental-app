from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from cars.models import Car, Booking
from decimal import Decimal

class CarViewsTest(TestCase):
    def setUp(self):
        # Create test data before each test
        self.car = Car.objects.create(
            make='Toyota',
            model='Camry',
            year=2020,
            price_per_day=Decimal('50.00'),
            available=True,
            # Add any other required fields from your Car model
        )
        
        # Create a test user if needed for authentication tests
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_car_list_view(self):
        response = self.client.get(reverse('cars:car_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.make)

    def test_car_detail_view(self):
        response = self.client.get(reverse('cars:car_detail', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.make)

    def test_booking_view_get(self):
        response = self.client.get(reverse('cars:book_car', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'customer_name')  # Check if form is present

    def test_booking_view_post(self):
        response = self.client.post(reverse('cars:book_car', args=[self.car.id]), {
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'customer_phone': '1234567890',
            'start_date': '2025-09-01',
            'end_date': '2025-09-03',
        })
        # Should redirect to payment page after successful booking
        self.assertEqual(response.status_code, 302)
        # Check that booking was created
        self.assertTrue(Booking.objects.filter(customer_email='john@example.com').exists())
