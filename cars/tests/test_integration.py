# Add this to your existing cars/tests.py file

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cars.models import Car, Booking

class CarRentalIntegrationTest(TestCase):
    """Integration tests for car rental workflow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test car (adjust fields to match your model)
        self.car = Car.objects.create(
            name="Test Car",
            brand="Toyota",
            year=2023,
            seats=5,
            location="Colombo",
            price_per_day=5000.00,
            description="Test car",
            available=True
        )

    def test_car_booking_workflow(self):
        """Test complete car booking process"""
        
        # Test car list page loads
        response = self.client.get(reverse('cars:car_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test car detail page
        response = self.client.get(reverse('cars:car_detail', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)
        
        # Test booking creation
        booking_data = {
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'customer_phone': '0771234567',
            'start_date': '2025-09-01',
            'end_date': '2025-09-05',
        }
        
        response = self.client.post(
            reverse('cars:book_car', args=[self.car.id]), 
            booking_data
        )
        
        # Check booking was created
        booking = Booking.objects.filter(car=self.car).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.customer_name, "John Doe")