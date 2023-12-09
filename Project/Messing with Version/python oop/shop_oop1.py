from dataclasses import dataclass, field
from typing import List
import csv

@dataclass
class Product:
    name: str
    price: float = 0.0

    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price})"

@dataclass 
class ProductStock:
    product: Product
    quantity: int

    def __repr__(self):
        return f"ProductStock(product={self.product}, quantity={self.quantity})"

@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

    def create_and_stock_shop(self):
        with open('../shop.csv') as csv_file:  
            csv_reader = csv.reader(csv_file, delimiter=',')  
            rows = list(csv_reader)
            self.cash = float(rows[0][0])

        with open('../stock.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, int(row[2]))
                self.stock.append(ps)

    def print_shop(self, customer):
        print(f'\nShop has {self.cash} in opening cash')
        for item in self.stock:
            print(item.product)
            print(f'The Shop has {item.quantity} of the above')
        customer.cost = sum(item.quantity * item.product.price for item in customer.shopping_list)

    def process_csv(self, customer):
        with open('../shop.csv', 'r') as shopcsv:
            reader = csv.reader(shopcsv)
            data = [row for row in reader]

        self.cash = float(data[0][0])
        customer.cost = sum(item.quantity * item.product.price for item in customer.shopping_list)
        result = self.perform_calculation(customer)
        data[0][0] = round(result, 2)
        print(f'\nAfter the above transaction, the Shop has a cash balance of: {result}')
        with open('../shop.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(data)

    def perform_calculation(self, customer):
        if customer.cost <= customer.budget:
            return self.cash + customer.cost
        else:
            return self.cash

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)
    cost: float = 0.00

    def read_customer(self, file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)        
            self.name = first_row[0]
            self.budget = float(first_row[1])

            # Read stock information once
            with open('../stock.csv') as stock_csv_file:
                stock_csv_reader = csv.reader(stock_csv_file, delimiter=',')
                stock_data = list(stock_csv_reader)

            for row in csv_reader:
                name = row[0]
                customer_quantity = int(row[1])

                # Search for the item in the stock data
                stock_item = next((stock_row for stock_row in stock_data if stock_row[0] == name), None)

                if stock_item is not None:
                    stock_name = stock_item[0]
                    price = float(stock_item[1])
                    stock_quantity = int(stock_item[2])

                    if customer_quantity > stock_quantity:
                        print(f"Warning: Insufficient stock for {stock_name}. Requested: {customer_quantity}, Available: {stock_quantity}")

                    p = Product(name, price)
                    ps = ProductStock(p, customer_quantity)
                    self.shopping_list.append(ps) 
                else:
                    print(f"Error: No stock information found for {name}")

    def live_order(self, shop):
        print("Welcome to the shop!")
        while True:
            product_name = input("Enter the product name (or 'done' to finish): ").strip().title()
            if product_name.lower() == 'done':
                break

            stock_item = next((item for item in shop.stock if item.product.name == product_name), None)
            if stock_item is None:
                print(f"Error: Product '{product_name}' not found in the shop's stock.")
                continue

            quantity = int(input(f"Enter the quantity of {product_name}: "))
            if quantity <= 0:
                print("Error: Quantity should be a positive integer.")
                continue

            if quantity > stock_item.quantity:
                print(f"Error: Insufficient stock for {product_name}. Available: {stock_item.quantity}")
                continue

            cost = quantity * stock_item.product.price
            print(f'The cost for {quantity} {product_name}(s) will be €{cost}')

            if cost > self.budget:
                print(f"Error: {self.name}, you cannot afford this order.")
                continue

            confirm_order = input("Do you want to confirm the order? (yes/no): ").lower()
            if confirm_order != 'yes':
                print("Order canceled.")
                continue

            self.cost += cost
            self.budget -= cost
            shop.cash += cost

            stock_item.quantity -= quantity

            ps = ProductStock(stock_item.product, quantity)
            self.shopping_list.append(ps)

            print(f"Order confirmed. Remaining budget: €{self.budget}, would you like anything else?")
            print("")

    def print_customer(self, shop):
        print(f'\nCUSTOMER NAME: {self.name} \nCUSTOMER BUDGET: {self.budget}')
        total_cost = 0
        valid_items = []  # List to store available items

        for item in self.shopping_list:
            # Check if the item is in the shop's stock
            stock_item = next((stock_item for stock_item in shop.stock if stock_item.product.name == item.product.name), None)
            stock_quantity = getattr(stock_item, 'quantity', 0)
            if stock_item is not None and stock_quantity != 0:
                print(stock_item.product)
                print(f'{self.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
                cost = int(item.quantity) * round(item.product.price, 2)
                self.cost += cost
                print(f'The cost to {self.name} will be €{cost}')
                total_cost += cost
                valid_items.append(item)
            else:
                print(f"The item '{item.product.name}' is not available in the shop's stock, therefore no charge will be applied.")

        self.shopping_list = valid_items  # Update shopping_list with valid items
        print(f' \nThe total cost to {self.name} will be €{total_cost}')

        # Check if the total cost exceeds the customer's budget
        if total_cost > self.budget:
            print(f'{self.name}, unfortunately, you cannot afford this order.')

# Executing code using attached csv files
shop = Shop()
customer = Customer()
shop.create_and_stock_shop()
customer.read_customer("../cust_shop_cant_fill.csv")

shop.live_order(customer)
shop.print_shop(customer)

try:
    customer.print_customer(shop)
except ValueError as e:
    print(f"Error: {e}")

shop.process_csv(customer)
