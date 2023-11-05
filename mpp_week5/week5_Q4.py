# MPP Week 5 Question 4
# Author Emma Dunleavy

# Create a class called “CollegeProgramme” which represents a programme of study which a student can be enrolled. 
# This class should have a “has many” relationship with another new class called “CollegeModule”. 
# Add other appropriate information and functionality to both classes, for example module name, number of credits, add a module to a programme etc.

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
    def __init__(self, name, age, home_address, college_course, module):
        super().__init__(name, age, home_address)
        self.college_course = college_course
        self.modules = [module]
        

    def set_college_address(self, college_address):
        self.add_address(college_address)                  

    def __repr__(self):
        return f"Student('{self.name}', {self.age}, '{self.college_course}' , {self.addresses})"
    
class CollegeProgramme(Student):
    def __init__(self, name, age,  home_address, college_course, module):
        super().__init__(name, age, home_address, college_course, module)

    def add_module(self, module):
        self.modules.append(module)
   
    def __repr__(self):
        home_address = self.addresses[0]
        college_address = self.addresses[1] if len(self.addresses) > 1 else home_address  
        return f"College Programme ('{self.college_course}' with '{self.name}', enrolled {self.age}, who lives at [{home_address}], [{college_address}] and taking {self.modules})"


home_address = Address("94", "Frenchcourt", "Orandale", "Galway", "H91K7P1")
college_address = Address("60", "Frenchpark", "Carrandale", "Mayo", "H91K7P2") #comment out to test no college address

#addresses = [address1, address2]

p1 = CollegeProgramme("Data Analytics", "John", 36, home_address, "MPP")
p1.set_college_address(college_address) #comment out to test no college address
p1.add_module("Fundametals of DA")

print(p1)