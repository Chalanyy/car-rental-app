import pytest
from cars.models import Car
from factory.django import DjangoModelFactory

class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car

    name = "Mitsubishi Lancer Ex"
    brand = "Mitsubishi"
    year = 2008
    seats = 5
    location = "Colombo"
    price_per_day = 4000.00
    description = "Used, well-maintained"
    main_image = "cars/default.jpg"  # use a placeholder image
    available = True


@pytest.mark.django_db
def test_car_creation():
    car = CarFactory()
    assert car.name == "Mitsubishi Lancer Ex"
    assert car.brand == "Mitsubishi"
    assert car.year == 2008
    assert car.seats == 5
    assert car.location == "Colombo"
    assert car.available is True  # this is my test models py
