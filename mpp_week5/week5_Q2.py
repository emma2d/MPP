# MPP Week 5 Question 2
# Author Emma Dunleavy

# Modify the Student class to extend the Person class which has been modified above. 
# This means the student should send an address to the parent class.

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def __repr__(self):
        return f"Person ('{self.name}', {self.age}, {self.address})"

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
    
class Student(Person):
    def __init__(self, name, age, college_course, address):
        super().__init__(name, age, address)
        self.college_course = college_course
        
             

    def __repr__(self):
        return f"Student('{self.name}', {self.age}, '{self.college_course}' , {self.address})"
     
address = Address("94", "Frenchcourt", "Orandale", "Galway", "H91K7P1")
#address2 = Address("60", "Frenchpark", "Carrandale", "Mayo", "H91K7P2")

#addresses = [address1, address2]

p1 = Student("John", 36, "MPP", address)

print(p1)