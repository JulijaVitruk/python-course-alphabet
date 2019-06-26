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

import json
import pickle
from ruamel.yaml import YAML
yaml = YAML()


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
    def from_serial_car(data):
        price = float(data['price'])
        car_type = data['car_type']
        producer = data['producer']
        mileage = float(data['mileage'])
        cr = Car(price=price, car_type=car_type, producer=producer, mileage=mileage)
        cr.number = data.get('number', False)
        return cr

    def to_serial_car(self):
        data = {"price": self.price, "car_type": self.car_type, "producer": self.producer, "mileage": self.mileage, \
                "number": self.number}
        return data

    def to_json_file(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self, file, default=Car.to_serial_car, indent=4)

    def to_json_str(self):
        return json.dumps(self, default=Car.to_serial_car)

    @staticmethod
    def from_json_file(file_name: str):
        with open(file_name, 'r') as file:
            car = json.load(file, object_hook=Car.from_serial_car)
        return car

    @staticmethod
    def from_json_str(ser_car: str):
        return json.loads(ser_car, object_hook=Car.from_serial_car)

    #Work with pickle
    def to_pickle_str(self):
        return pickle.dumps(self)

    def to_pickle_file(self, file_name: str):
        with open(file_name, 'w') as file:
            pickle.dump(self, file)

    @staticmethod
    def from_pickle_str(ser_car):
        return pickle.loads(ser_car)

    @staticmethod
    def from_pickle_file(file_name: str):
        with open(file_name, 'r') as file:
            car = pickle.load(file)
        return car

    #Work with Yaml
    def to_yaml_file(self, file_name: str):
        with open(file_name, 'w') as file:
            yaml.dump(self.to_serial_car(), file)

    @staticmethod
    def from_yaml_file(file_name: str):
        with open(file_name, 'r') as file:
            data = yaml.load(file)
        return Car.from_serial_car(data)



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
    def from_serial_garage(data1):
        cars = data1['cars']
        town = data1['town']
        places = data1['places']
        gr = Garage(town=town, places=places)
        gr.owner = data1.get('owner')
        gr.current = data1.get('current')
        for car in cars:
            crs = Car.from_serial_car(car)
            gr.add(crs)
        return gr

    def to_serial_garage(self):
        m = []
        for car in self.cars:
            m.append(car.to_serial_car())
        data = {'town': self.town, "places": self.places, "cars": m, "owner": self.owner,
                "current": self.current}
        return data

    def to_json_file(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self, file, default=Garage.to_serial_garage, indent=4)

    def to_json_str(self):
        return json.dumps(self, default=Garage.to_serial_garage)

    @staticmethod
    def from_json_file(file_name: str):
        with open(file_name, 'r') as file:
            lod_gar = json.load(file)
        return Garage.from_serial_garage(lod_gar)

    @staticmethod
    def from_json_str(ser_gar: str):
        lod_gar = json.loads(ser_gar)
        return Garage.from_serial_garage(lod_gar)

    # Work with pickle
    def to_pickle_str(self):
        return pickle.dumps(self)

    def to_pickle_file(self, file_name: str):
        with open(file_name, 'w') as file:
            pickle.dump(self, file)

    @staticmethod
    def from_pickle_str(ser_garage):
        return pickle.loads(ser_garage)

    @staticmethod
    def from_pickle_file(file_name: str):
        with open(file_name, 'r') as file:
            garage = pickle.load(file)
        return garage

    #Work with Yaml
    def to_yaml_file(self, file_name: str):
        with open(file_name, 'w') as file:
            yaml.dump(self.to_serial_garage(), file)

    @staticmethod
    def from_yaml_file(file_name: str):
        with open(file_name, 'r') as file:
            data = yaml.load(file)
        return Garage.from_serial_garage(data)

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
    @staticmethod
    def from_serial_cesar(data):
        name = data['name']
        garages = data['garages']
        list_of_garages = []
        for gar in garages:
            grs = Garage.from_serial_garage(gar)
            list_of_garages.append(grs)
        cesr = Cesar(name=name, garages=list_of_garages)
        cesr.register_id = data.get('register_id')
        cesr.current = data.get('current')

        return cesr

    def to_serial_cesar(self):
        m = []
        for garage in self.garages:
            m.append(garage.to_serial_garage())
        data = {"name": self.name, "garages": m, "register_id": self.register_id,
                "current": self.current}
        return data

    def to_json_file(self, file_name: str):
        with open(file_name, 'w') as file:
            json.dump(self, file, default=Cesar.to_serial_cesar, indent=4)

    def to_json_str(self):
        return json.dumps(self, default=Cesar.to_serial_cesar)

    @staticmethod
    def from_json_file(file_name: str):
        with open(file_name, 'r') as file:
            lod_ces = json.load(file)
        return Cesar.from_serial_cesar(lod_ces)

    @staticmethod
    def from_json_str(ser_ces: str):
        lod_ces = json.loads(ser_ces)
        return Cesar.from_serial_cesar(lod_ces)

    # Work with pickle
    def to_pickle_str(self):
        return pickle.dumps(self)

    def to_pickle_file(self, file_name: str):
        with open(file_name, 'w') as file:
            pickle.dump(self, file)

    @staticmethod
    def from_pickle_str(ser_cesar):
        return pickle.loads(ser_cesar)

    @staticmethod
    def from_pickle_file(file_name: str):
        with open(file_name, 'r') as file:
            cesar = pickle.load(file)
        return cesar

    #Work with Yaml
    def to_yaml_file(self, file_name: str):
        with open(file_name, 'w') as file:
            yaml.dump(self.to_serial_cesar(), file)

    @staticmethod
    def from_yaml_file(file_name: str):
        with open(file_name, 'r') as file:
            data = yaml.load(file)
        return Cesar.from_serial_cesar(data)

if __name__ == '__main__':
    print("\nWork with Cars")

    car1 = Car(23.0, 'SUV', 'Lamborghini', 765.4)
    car1.to_yaml_file('yaml_car.yaml')
    car5 = Car.from_yaml_file('yaml_car.yaml')
    print('car5 from yaml', car5)

    car2 = Car(14.6, 'Sedan', 'Ford', 560.7)
    ser_car1 = car1.to_json_str()
    print(ser_car1)
    car3 = Car.from_json_str(ser_car1)
    print(id(car1), car1, '\n', id(car3), car3)
    car2.to_json_file('json_car.json')
    car4 = Car.from_json_file('json_car.json')
    print(id(car2), car2, '\n', id(car4), car4)


    print("\nWork with Garages")
    garage1 = Garage("Kiev", 45)

    garage1.add(car1)
    garage1.add(car2)
    car3 = Car(45.0, "Sedan", "Ford", 200.0)
    garage1.add(car3)
    ser_garage1 = garage1.to_json_str()
    print(ser_garage1)
    garage3 = Garage.from_json_str(ser_garage1)
    print(id(garage1), garage1, '\n', id(garage3), garage3)

    garage2 = Garage('Rome', 17)
    garage2.add(car3)
    garage2.add(car4)
    garage2.to_json_file('json_garage.json')
    garage4 = Garage.from_json_file('json_garage.json')
    print(id(garage2), garage2, '\n', id(garage4), garage4)


    print("\nWork with Cesar")

    cesar1 = Cesar('Harrison Ford', [garage1, garage2])
    print(cesar1)

    ser_cesar1 = cesar1.to_json_str()
    print(ser_cesar1)
    cesar3 = Cesar.from_json_str(ser_cesar1)
    print(id(cesar1), cesar1, '\n', id(cesar3), cesar3)
    cesar2 = Cesar('Vitruk Julija', [garage2, garage4])
    cesar2.to_json_file('json_cesar.json')
    cesar4 = Cesar.from_json_file('json_cesar.json')
    print(id(cesar2), cesar2, '\n', id(cesar4), cesar4)
    ser_cesar3 = cesar3.to_pickle_str()
    print(ser_cesar3)
    cesar5 = Cesar.from_pickle_str(ser_cesar3)
    print(cesar5, cesar5.garages)



