from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),  # function-based
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('receipts/<int:booking_id>/', views.receipt, name='receipt'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.contact, name='contact'),
]
