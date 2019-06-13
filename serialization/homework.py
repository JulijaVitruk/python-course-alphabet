"""
Для попереднього домашнього завдання.
Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) файлу відповідно

Для класів Колекціонер Машина і Гараж написати методи, які зберігають стан обєкту в файли формату
yaml, json, pickle відповідно.

Для класів Колекціонер Машина і Гараж написати методи, які конвертують обєкт в строку формату
yaml, json, pickle відповідно.

Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) строки відповідно


Advanced
Добавити опрацьовку формату ini

"""
from __future__ import annotations
from typing import List
import uuid
from serialization.constants import CARS_PRODUCER, CARS_TYPES, TOWNS
from serialization.lesson.json_example.json_utils import JsonEncoder, json_hook
import json


class Car:
    """
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

    # Work with json
    @staticmethod
    def from_json_car(data):
        price = data['price']
        car_type = data['car_type']
        producer = data['producer']
        mileage = data['mileage']
        cr = Car(price=price, car_type=car_type, producer=producer, mileage=mileage)
        cr.number = data.get('number', False)
        return cr

    '''
    @staticmethod
    def to_json_car(obj: Car):
        data = {"price": obj.price, "car_type": obj.car_type, "producer": obj.producer, "mileage": obj.mileage, \
                "number": obj.number}
        return data
    '''

    def to_json_car(self):
        data = {"price": self.price, "car_type": self.car_type, "producer": self.producer, "mileage": self.mileage, \
                "number": self.number}
        return data

    def to_json_file(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self, file, default=Car.to_json_car, indent=4)

    def to_json_str(self):
        return json.dumps(self, default=Car.to_json_car)

    @staticmethod
    def from_json_file(file_name: str):
        with open(file_name, 'r') as file:
            car = json.load(file, object_hook=Car.from_json_car)
        return car

    @staticmethod
    def from_json_str(cls, ser_car: str):
        return json.loads(ser_car, object_hook=Car.from_json_car)


class Garage:
    """
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

    #Work with json
    @staticmethod
    def from_json_garage(data1):

        cars = data1["cars"]
        town = data1['town']
        places = data1["places"]
        gr = Garage(town=town, places=places)
        gr.owner = data1.get('owner')
        gr.current = data1.get('current')
        crs = []
        for i, car in enumerate(cars):
            crs[i] = Car.from_json_car(car)
            gr.add(crs[i])
        return gr

    def to_json_garage(self):
        m = []
        for car in self.cars:
            m.append(car.to_json_car())
        data = {'town': self.town, "places": self.places, "cars": m, "owner": self.owner,
                "current": self.current}
        return data

    def to_json_file(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self, file, default=Garage.to_json_garage, indent=4)

    def to_json_str(self):
        return json.dumps(self, default=Garage.to_json_garage)

    @staticmethod
    def from_json_file(file_name: str):
        with open(file_name, 'r') as file:
            garage = json.load(file, object_hook=Garage.from_json_garage)
        return garage

    @staticmethod
    def from_json_str(ser_gar: str):
        return json.loads(ser_gar, object_hook=Garage.from_json_garage)


class Cesar:
    """

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

    #Work with json
    @classmethod
    def from_json(cls, data):
        name = data['name']
        garages = data['garages']
        cesr = Cesar(name=name, garages=garages)
        cesr.register_id = data.get('register_id')
        cesr.current = data.get('current')
        return cesr


    @staticmethod
    def to_json(obj: Cesar):
        data = {"name": obj.name, "garages": obj.garages, "register_id": obj.register_id, "current": obj.current}
        return data

    def to_json_file(self, file_name: str, indent=4):
        with open(file_name, 'w') as file:
            json.dump(self, file, default=Cesar.to_json)

    def to_json_str(self):
        return json.dumps(self, default=Cesar.to_json)

    @classmethod
    def from_json_file(cls, file_name: str):
        with open(file_name, 'r') as file:
            cesar = json.load(file, object_hook=Cesar.from_json)
        return cesar

    @classmethod
    def from_json_str(cls, ser_ces: str):
        return json.loads(ser_ces, object_hook=Cesar.from_json)

if __name__ == '__main__':
    print("\nWork with Cars")

    car1 = Car(23.0, 'SUV', 'Lamborghini', 765.4)

    car2 = Car(14.6, 'Sedan', 'Ford', 560.7)
    ser_car1 = car1.to_json_str()
    """print(ser_car1)
    car3 = Car.from_json_str(ser_car1)
    print(id(car1), car1, '\n', id(car3), car3)
    car2.to_json_file('json_car.json')
    car4 = Car.from_json_file('json_car.json')
    print(id(car2), car2, '\n', id(car4), car4)"""


    print("\nWork with Garages")
    garage1 = Garage("Kiev", 45)

    garage1.add(car1)
    garage1.add(car2)
    car3 = Car(45.0, "Sedan", "Ford", 200.0)
    garage1.add(car3)

    ser_garage1 = garage1.to_json_str()
    print(ser_garage1)
    garage2 = Garage.from_json_str(ser_garage1)






    """
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
    """

