from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView, TemplateView
from .models import Car, Booking, Payment, Review
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import EmailAuthenticationForm, ProfileForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required

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
    
    if booking.is_paid:
        messages.info(request, 'This booking has already been paid.')
        return redirect("cars:receipt", booking_id=booking.id)

    if request.method == "POST":
        card_number = (request.POST.get("card_number") or "").replace(" ", "")
        cardholder_name = (request.POST.get("cardholder_name") or "").strip()
        expiry_date = (request.POST.get("expiry_date") or "").strip()
        cvv = (request.POST.get("cvv") or "").strip()

        errors = []
        if len(card_number) < 13 or len(card_number) > 19:
            errors.append("Invalid card number.")
        if not cardholder_name:
            errors.append("Cardholder name is required.")
        if not expiry_date or len(expiry_date) != 5:
            errors.append("Invalid expiry date format (MM/YY).")
        if not cvv or len(cvv) < 3:
            errors.append("Invalid CVV.")

        if errors:
            return render(request, "cars/payment.html", {
                "booking": booking, 
                "errors": errors
            })

        Payment.objects.create(
            booking=booking,
            cardholder_name=cardholder_name,
            card_last4=card_number[-4:],
            amount=booking.total_amount,
        )

        booking.is_paid = True
        booking.save()

        messages.success(request, 'Payment processed successfully!')
        return redirect("cars:receipt", booking_id=booking.id)

    return render(request, "cars/payment.html", {"booking": booking})

# ===== RECEIPT =====
def receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment = Payment.objects.filter(booking=booking).first()
    return render(request, 'cars/receipt.html', {
        'booking': booking,
        'payment': payment,
    })

# ===== ABOUT =====
def about_view(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        comment = request.POST.get('comment', '').strip()
        if name and comment:
            Review.objects.create(name=name, comment=comment)
            messages.success(request, 'Thank you for your review!')
            return redirect('cars:about')

    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'cars/about.html', {'reviews': reviews})

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

# ===== SERVICES =====
def services(request):
    context = {
        'page_title': 'Our Services',
        'services_list': [
            {'title': 'Daily Car Rental', 'description': 'Rent a car for your daily needs', 'icon': 'fas fa-car'},
            {'title': 'Weekly Rentals', 'description': 'Extended rental options for longer stays', 'icon': 'fas fa-calendar-week'},
            {'title': 'Airport Transfers', 'description': 'Pickup and drop-off services', 'icon': 'fas fa-plane'},
            {'title': '24/7 Support', 'description': 'Customer support anytime', 'icon': 'fas fa-headset'},
            {'title': 'GPS Navigation', 'description': 'Cars with GPS systems', 'icon': 'fas fa-map-marked-alt'},
            {'title': 'Insurance Coverage', 'description': 'Comprehensive insurance', 'icon': 'fas fa-shield-alt'},
        ]
    }
    return render(request, 'cars/services.html', context)

# ===== AUTHENTICATION AND PROFILE =====
class CustomLoginView(LoginView):
    template_name = 'cars/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('admin:index')
        return reverse_lazy('cars:car_list')

def profile(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        if not request.user.is_authenticated:
            return redirect('login')
        profile_user = request.user
    return render(request, 'cars/profile.html', {'profile_user': profile_user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'cars/edit_profile.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'cars/change_password.html'  # Fixed syntax
    success_url = reverse_lazy('my_profile')

def login_view(request):
    return render(request, 'cars/login.html')
    
@login_required
def payment_list(request):
    payments = Payment.objects.filter(booking__customer_email=request.user.email)
    return render(request, 'cars/payment_list.html', {'payments': payments})

@login_required
def receipt_list(request):
    bookings = Booking.objects.filter(customer_email=request.user.email)
    return render(request, 'cars/receipt_list.html', {'bookings': bookings})

