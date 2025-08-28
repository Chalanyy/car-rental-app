from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView, DetailView, TemplateView
from .models import Car, Booking, Payment
from datetime import datetime
from decimal import Decimal

# ===== HOME PAGE =====
class HomeView(TemplateView):
    template_name = 'cars/home.html'

# ===== CAR VIEWS =====
class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return Car.objects.filter(available=True)

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'cars/car_detail.html', {'car': car})

# ===== BOOKING =====
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        customer_email = request.POST.get("customer_email", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        start_date = request.POST.get("start_date", "").strip()
        end_date = request.POST.get("end_date", "").strip()

        if not (customer_name and customer_email and start_date and end_date):
            return render(request, "cars/book_car.html", {"car": car, "error": "Please fill all required fields."})

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "cars/book_car.html", {"car": car, "error": "Invalid date format."})

        days = (end - start).days
        if days <= 0:
            return render(request, "cars/book_car.html", {"car": car, "error": "End date must be after start date."})

        total_amount = Decimal(days) * car.price_per_day

        booking = Booking.objects.create(
            car=car,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            start_date=start,
            end_date=end,
            total_amount=total_amount,
        )

        return redirect("cars:payment", booking_id=booking.id)

    return render(request, "cars/book_car.html", {"car": car})

# ===== PAYMENT =====
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        card_number = (request.POST.get("card_number") or "").replace(" ", "")
        cardholder_name = request.POST.get("cardholder_name") or ""

        if len(card_number) < 4:
            return render(request, "cars/payment.html", {"booking": booking, "error": "Invalid card number."})

        # Save minimal payment info
        Payment.objects.create(
            booking=booking,
            cardholder_name=cardholder_name,
            card_last4=card_number[-4:],
            amount=booking.total_amount,
        )

        booking.is_paid = True
        booking.save()

        return redirect("cars:receipt", booking_id=booking.id)

    return render(request, "cars/payment.html", {"booking": booking})

# ===== RECEIPT =====
def receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "cars/receipt.html", {"booking": booking})

# ===== ABOUT =====
class AboutView(TemplateView):
    template_name = 'cars/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'About Us',
            'company_name': 'GoRydz Car Rental',
            'founded_year': '2020',
            'total_cars': Car.objects.count(),
            'total_bookings': Booking.objects.count(),
        })
        return context

# ===== CONTACT =====
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            try:
                full_message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
                send_mail(
                    subject=f'Contact Form: {subject}',
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you! We will contact you soon.')
                return redirect('cars:contact')
            except Exception:
                messages.error(request, 'Error sending message.')
        else:
            messages.error(request, 'Please fill all fields.')

    return render(request, 'cars/contact.html', {
        'page_title': 'Contact Us',
        'phone': '+94 77 123 4567',
        'email': 'info@gorydz.com',
        'address': '123 Main Street, Negombo, Sri Lanka',
        'business_hours': {'weekdays': '8:00-22:00', 'saturday': '8:00-22:00', 'sunday': '8:00-22:00'},
    })
