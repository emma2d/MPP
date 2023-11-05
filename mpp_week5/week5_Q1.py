# MPP Week 5 Question 1
# Author Emma Dunleavy

# Modify the Person class, from the lecture notes, such that a person can have multiple addresses. 
# You can use a list for this purpose. Add a method to the Person class to add a new address.

class Person:
    def __init__(self, name, age, addresses):
        self.name = name
        self.age = age
        self.addresses = addresses

    def __repr__(self):
        return f"Person ('{self.name}', {self.age}, {self.addresses})"

class Address:
    def __init__(self, house_number, street, town, county, eircode, country="Ireland"):
        self.house_number = house_number
        self.street = street
        self.town = town
        self.county = county
        self.eircode = eircode
        self.country = country

    def __repr__(self):      
        return f"Address ('{self.house_number}','{self.street}',\n'{self.town}',\n'{self.county}',\n'{self.eircode}',\n'{self.country}')"
    

     
address1 = Address("94", "Frenchcourt", "Orandale", "Galway", "H91K7P1")
address2 = Address("60", "Frenchpark", "Carrandale", "Mayo", "H91K7P2")

addresses = [address1, address2]

p1 = Person("John", 36, addresses)

print(p1)