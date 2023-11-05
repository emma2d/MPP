# MPP Week 5 Question 3
# Author Emma Dunleavy

# Modify the program from Q2 such that the Student has methods to access their home address and college address. 
# This should use the list from the parent class. If there is only 1 address then the college address will be the same as the home address.

class Person:
   
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.addresses = [address]

    def add_address(self, address):
        self.addresses.append(address)

    def get_home_address(self):
        return self.addresses[0]

    def get_college_address(self):
        if len(self.addresses) > 1:
            return self.addresses[-1]
        else:
            return self.addresses[0]

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
        return f"Address ('{self.house_number}','{self.street}','{self.town}','{self.county}','{self.eircode}','{self.country}')"
    
class Student(Person):
    def __init__(self, name, age, college_course, home_address):
        super().__init__(name, age, home_address)
        self.college_course = college_course

    def set_college_address(self, college_address):
        self.add_address(college_address)            

    def __repr__(self):
        return f"Student('{self.name}', {self.age}, '{self.college_course}' , {self.addresses})"
     
home_address = Address("94", "Frenchcourt", "Orandale", "Galway", "H91K7P1")
college_address = Address("60", "Frenchpark", "Carrandale", "Mayo", "H91K7P2") #comment out to test no college address

#addresses = [address1, address2]

p1 = Student("John", 36, "MPP", home_address)
p1.set_college_address(college_address) #comment out to test no college address

print(p1)