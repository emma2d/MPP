from dataclasses import dataclass, field
from typing import List
import csv

@dataclass
class Product:
    name: str
    price: float = 0.0

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}"

@dataclass 
class ProductStock:
    product: Product
    quantity: int

    def __repr__(self):
        return f"ProductStock(product={self.product}, quantity={self.quantity}"

@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

def create_and_stock_shop():
    s = Shop()
    
    # Read prices from a separate CSV file
    with open('../stock.csv') as prices_file:
        prices_reader = csv.reader(prices_file, delimiter=',')
        price_dict = {row[0]: float(row[1]) for row in prices_reader}

    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            product_name = row[0]
            quantity = float(row[2])
            
            # Use the price from the dictionary
            price = price_dict.get(product_name, 0.0)
            
            p = Product(product_name, price)
            ps = ProductStock(p, quantity)
            s.stock.append(ps)
            print(ps)
    return s
    
def read_customer(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        return c 
        

def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

def print_customer(c):
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    
    for item in c.shopping_list:
        print_product(item.product)
        
        print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
        cost = item.quantity * item.product.price
        print(f'The cost to {c.name} will be €{cost}')
        
def print_shop(s):
    print(f'Shop has {s.cash} in cash')
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')

s = create_and_stock_shop()
print_shop(s)

c = read_customer("../customer.csv")
print_customer(c)