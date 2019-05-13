from __future__ import annotations
from typing import List
import uuid
import constants

"""
Вам небхідно написати 3 класи. Колекціонери Гаражі та Автомобілі.
Звязкок наступний один колекціонер може мати багато гаражів.
В одному гаражі може знаходитися багато автомобілів.
"""


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
    def __init__(self, price: float, car_type, producer, mileage: float) -> None:
        self.price = price
        self.number = uuid.uuid4().hex
        self.mileage = mileage
        if car_type in constants.CARS_TYPES:
            self.car_type = car_type
        else:
            print("Value of car_type must be in CARS_TYPES:",constants.CARS_TYPES)
            raise ValueError

        if producer in constants.CARS_PRODUCER:
            self.producer = producer
        else:
            print("Value of producer must be in CARS_PRODUCER",constants.CARS_PRODUCER)
            raise ValueError
        print("We create new car", self.price, self.car_type, self.producer, self.mileage, self.number)

    def __new__(cls, *args, **kwargs):
        obj = super(Car, cls).__new__(cls)
        return obj

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


print("\nWork with Cars")
car1 = Car(23, 'SUV', 'Lamborghini', 765)
car2 = Car(34, "Sedan", "Ford", 1042)
print(car1.number, car1.car_type, car1.mileage, car1.price, car1.producer)
print(car1 <= car2)
car1.change_number()
print(car1.number)


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

    def __init__(self, town, places: int, cars=None):

        if town in constants.TOWNS:
            self.town = town
        else:
            print("Value of town must be in TOWNS:",constants.TOWNS)
            raise ValueError

        self.places = places
        self.cars = cars if cars is not None else []
        self.owner = uuid.uuid4().hex
        self.current = 0

    def __new__(cls, *args, **kwargs):

        print("We create new garage")
        obj = super(Garage, cls).__new__(cls)
        return obj

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

    def add(self, new_car: Car):
        if len(self.cars) < self.places:
            self.cars.append(new_car)
        else:
            print("The garage is already full")

    def remove(self, car: Car):
        if car in self.cars:
            self.cars.remove(car)
        else: print("This car is not in garage")

    def hit_hat(self):
        return sum([x.price for x in self.cars])

    def count(self):
        return len(self.cars)


print("\n Work with Garages")
garage1 = Garage('Kiev', 10)
print(garage1.cars)
garage1.add(car1)
garage1.add(car2)
car3 = Car(45, "Sedan", "Ford", 200)
garage1.add(car3)
print(garage1.cars)
print(garage1.hit_hat())
garage1.remove(car2)
for i in garage1:
    print(i.producer, i.car_type, i.price)


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

        self.name = name
        self.garages = garages if garages is not None else []
        self.register_id = uuid.uuid4().hex
        self.current = 0

    def __new__(cls, *args, **kwargs):

        print("We create new cesar")
        obj = super(Cesar, cls).__new__(cls)
        return obj

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


print("\nWork with Cesar")
garage2 = Garage('Kiev', 2, [car2])
cesar1 = Cesar('Harrison Ford', [garage1, garage2])
print(cesar1.name, cesar1.garages)
print(cesar1.hit_hat())
print(cesar1.garages_count())
print(cesar1.cars_count())
car4 = Car(25, 'Sedan', 'BMW', 450)
cesar1.add_car(car4, garage1)
print(cesar1.hit_hat())


