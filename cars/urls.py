from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'cars'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('receipt/<int:booking_id>/', views.receipt, name='receipt'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='my_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(next_page='cars:home'), name='logout'),
    path('payments/', views.payment_list, name='payment_list'),
    path('receipts/', views.receipt_list, name='receipt_list'),
]