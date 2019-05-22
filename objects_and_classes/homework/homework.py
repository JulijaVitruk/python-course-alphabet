from __future__ import annotations
from typing import List
import uuid
from constants import CARS_PRODUCER, CARS_TYPES, TOWNS


class Car:
    """
    Автомобіль має наступні характеристики:
    price - значення типу float. Всі ціни за дефолтом в одній валюті.
    type - одне з перерахованих значеннь з CARS_TYPES в docs.
    producer - одне з перерахованих значень в CARS_PRODUCER.
    number - значення типу UUID. Присвоюється автоматично при створенні автомобілю.
    mileage - значення типу float. Пробіг автомобіля в кілометрах.

    Автомобілі можна порівнювати між собою за ціною.
    При виводі(logs, print) автомобілю повинні зазначатися всі його атрибути.

    Автомобіль має метод заміни номеру. номер повинен відповідати UUID
    """
    def __init__(self, price: float, car_type: str, producer: str, mileage: float) -> None:

        assert type(price) is float, 'Value of price must be float'
        self.price = price

        self.number = uuid.uuid4().hex

        assert type(mileage) is float, 'Value of mileage must be float'
        self.mileage = mileage

        assert car_type in CARS_TYPES, "Value of car_type must be in CARS_TYPES: %s" % CARS_TYPES
        self.car_type = car_type

        assert producer in CARS_PRODUCER, "Value of producer must be in CARS_PRODUCER: %s" % CARS_PRODUCER
        self.producer = producer

    def __eq__(self, other: Car):
        return other.price == self.price

    def __le__(self, other: Car):
        return self.price <= other.price

    def __lt__(self, other: Car):
        return self.price < other.price

    def __ge__(self, other: Car):
        return self.price >= other.price

    def __gt__(self, other: Car):
        return self.price > other.price

    def change_number(self):
        # Метод заміни номеру
        self.number = uuid.uuid4().hex

    def __str__(self):
        return str(self.price) + " " + str(self.car_type) + " " + str(self.producer) + " " + str(self.mileage) + " "\
               + str(self.number)


class Garage:
    """
    Гараж має наступні характеристики:

    town - одне з перечислених значеннь в TOWNS
    cars - список з усіх автомобілів які знаходяться в гаражі
    places - значення типу int. Максимально допустима кількість автомобілів в гаражі
    owner - значення типу UUID. За дефолтом None.

    Повинен мати реалізованими наступні методи

    add(car) -> Добавляє машину в гараж, якщо є вільні місця
    remove(car) -> Забирає машину з гаражу.
    hit_hat() -> Вертає сумарну вартість всіх машин в гаражі
    """
    cars: List[Car]

    def __init__(self, town: str, places: int, cars=None):

        assert town in TOWNS, "Value of town must be in TOWNS: %s" % TOWNS
        self.town = town

        assert type(places) is int, 'Value of places must be integer'
        self.places = places

        self.cars = cars if cars is not None else []

        self.owner = uuid.uuid4().hex

        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.current < len(self.cars):
            res = self.cars[self.current]
            self.current += 1
            return res
        else:
            self.current = 0
            raise StopIteration

    def __contains__(self, item):
        return item in self.cars

    def __str__(self):
        return str(self.town) + ' ' + str(self.places) + ' ' + str(self.owner)

    def add(self, new_car: Car):
        if len(self.cars) < self.places:
            self.cars.append(new_car)
        else:
            print("The garage is already full")

    def remove(self, car: Car):
        if car in self.cars:
            self.cars.remove(car)
        else:
            print("This car is not in garage")

    def hit_hat(self):
        return sum([x.price for x in self.cars])

    def count(self):
        return len(self.cars)


class Cesar:
    """
    Колекціонер має наступні характеристики
    name - значення типу str. Його ім'я
    garages - список з усіх гаражів які належать цьому Колекціонеру. Кількість гаражів за замовчуванням - 0
    register_id - UUID; Унікальна айдішка Колекціонера.

    Повинні бути реалізовані наступні методи:
    hit_hat() - повертає ціну всіх його автомобілів.
    garages_count() - вертає кількість гаріжів.
    сars_count() - вертає кількість машиню
    add_car() - додає машину у вибраний гараж. Якщо гараж не вказаний, то додає в гараж, де найбільше вільних місць.
    Якщо вільних місць немає повинне вивести повідомлення про це.

    Колекціонерів можна порівнювати за ціною всіх їх автомобілів.
    """
    garages: List[Garage]

    def __init__(self, name: str, garages=None):

        assert type(name) is str, 'Value of name must be string'
        self.name = name

        self.garages = garages if garages is not None else []
        self.register_id = uuid.uuid4().hex
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.current < len(self.garages):
            res = self.garages[self.current]
            self.current += 1
            return res
        else:
            self.current = 0
            raise StopIteration

    def __contains__(self, item):
        return item in self.garages

    def hit_hat(self):
        return sum([x.hit_hat() for x in self.garages])

    def __eq__(self, other: Cesar):
        return other.hit_hat() == self.hit_hat()

    def __le__(self, other: Cesar):
        return self.hit_hat() <= other.hit_hat()

    def __lt__(self, other: Cesar):
        return self.hit_hat() < other.hit_hat()

    def __ge__(self, other: Cesar):
        return self.hit_hat() >= other.hit_hat()

    def __gt__(self, other: Cesar):
        return self.hit_hat() > other.hit_hat()

    def __str__(self):
        return str(self.name) + ' ' + str(self.register_id)

    def garages_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum([garage.count() for garage in self.garages])

    def add_car(self, car: Car, garage: None):
        if garage is not None:
            garage.add(car)
        else:
            list_garage_count = [x.count() for x in self.garages]
            garage = self.garages[list_garage_count.index(min(list_garage_count))]
            garage.add(car)


if __name__ == '__main__':
    print("\nWork with Cars")

    car1 = Car(23.0, 'SUV', 'Lamborghini', 765.4)
    car2 = Car(34.0, "Sedan", "Ford", 1042.9)
    print(car1)
    print(car2)
    print(car1 <= car2)
    car1.change_number()
    print(car1)

    print("\nWork with Garages")
    garage1 = Garage("Kiev", 45)
    print(garage1)
    garage1.add(car1)
    garage1.add(car2)
    car3 = Car(45.0, "Sedan", "Ford", 200.0)
    garage1.add(car3)
    print(garage1.hit_hat())
    for i in garage1:
        print(i.producer, i.car_type, i.price)
    garage1.remove(car2)
    for i in garage1:
        print(i.producer, i.car_type, i.price)

    print("\nWork with Cesar")
    garage2 = Garage('Kiev', 2, [car2])
    cesar1 = Cesar('Harrison Ford', [garage1, garage2])
    print(cesar1)
    print(cesar1.name, cesar1.garages)
    print(cesar1.hit_hat())
    print(cesar1.garages_count())
    print(cesar1.cars_count())
    car4 = Car(25.5, 'Sedan', 'BMW', 450.8)
    cesar1.add_car(car4, garage1)
    print(cesar1.hit_hat())

