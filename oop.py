# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 09:58:21 2025

@author: U S E R
"""

#pythonda OOP ni ishlatish
class Car():
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color
        
    def drive(self):
            print(f"{self.brand} {self.color} harakatlanmoqda!")
    
#obyekt yaratamiz
car1 = Car("BMW", "Black")
car2=Car("Nexia", "White")

car1.drive()
car2.drive()

class Animal():
    def __init__(self, name):
        self.name = name
        
    def speak(self):
        print(f"{self.name} ovoz chiqarmoqda")
        
#Animal kalsidan meors olamiz
class Cat(Animal):
    def speak(self):
        print(f"{self.name} miyovlamoqda")
cat1 = Cat("Tom")
cat1.speak()
#Escapsulation - kdlarni yashirish
class Bankaccount():
    def __init__(self, balance):
        self.__balance = balance
        
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
    
    def get_balance(self):
        return self.balance

account = Bankaccount(1000)

account.deposit(500)
print(account.get_balance())



















