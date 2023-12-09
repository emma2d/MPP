
from dataclasses import dataclass, field
from typing import List
import csv

@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass
class ProductStock:
    product: Product
    quantity: int

@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)
    cost: float = 0.0

# Create a shop instance and populate it with stock information from a CSV file.
def create_and_stock_shop():
    s = Shop()
    with open('../shop.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows = list(csv_reader)
        s.cash = float(rows[0][0])

    with open('../stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, int(row[2]))
            s.stock.append(ps)
    return s

# Read customer information from a CSV file and create a customer instance.
def read_customer_live_order(s):
    print("Welcome to the shop!")
    customer_name = input("Enter customer name: ")
    customer_budget = float(input("Enter customer budget: "))
    c = Customer(name=customer_name, budget=customer_budget)

    while True:
        product_name = input("Shop Menu: Coke Can, Bread, Spaghetti, Tomato Sauce, Bin Bags, Jam, Bananas. Enter the product name (or 'done' to finish): ").strip().title()
        if product_name.lower() == 'done':
            break

        stock_item = next((item for item in s.stock if item.product.name == product_name), None)
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
        print(f'The cost for {quantity} {product_name}(s) will be €{round(cost):.2f}')

        if cost > c.budget:
            print(f"Error: {c.name}, you cannot afford this order.")
            continue

        confirm_order = input("Do you want to confirm the order? (y/n): ").lower()
        if confirm_order != 'y':
            print("Order canceled.")
            continue

        c.cost += cost
        c.budget -= cost
        s.cash += cost

        stock_item.quantity -= quantity

        ps = ProductStock(stock_item.product, quantity)
        c.shopping_list.append(ps)

        print(f"Order confirmed. Remaining budget: €{round(c.budget):.2f}, would you like anything else?")
        print("")

    return c

def read_customer_from_csv(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))

        # Assuming the CSV file contains product names and quantities
        for row in csv_reader:
            name = row[0]
            customer_quantity = int(row[1])

            # Assuming the stock information is read from 'stock.csv'
            with open('../stock.csv') as stock_csv_file:
                stock_csv_reader = csv.reader(stock_csv_file, delimiter=',')
                stock_data = list(stock_csv_reader)

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
                c.shopping_list.append(ps)
            else:
                print(f"Error: No stock information found for {name}")

    return c

# Print product information.
def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

# Perform cash calculation based on the order.
def perform_calculation(shop: Shop, customer: Customer):
    if customer.cost <= customer.budget:
        return shop.cash + customer.cost
    else:
        return shop.cash

# Print shop information, including opening cash and current stock.
def print_shop(s, c):
    print(f'\nShop has {s.cash} in opening cash')
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
    c.cost = sum(item.quantity * item.product.price for item in c.shopping_list)

# Process the CSV file, update the shop's cash balance, and write the result back to the file.
def process_csv(c):
    s = Shop()
    with open('../shop.csv', 'r') as shopcsv:
        reader = csv.reader(shopcsv)
        data = [row for row in reader]

    s.cash = float(data[0][0])
    c.cost = sum(item.quantity * item.product.price for item in c.shopping_list)
    result = perform_calculation(s, c)
    data[0][0] = round(result, 2)
    print(f'\nAfter the above transaction, the Shop has a cash balance of: {round(result):.2f}')
    with open('../shop.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)

def print_customer(c, s):
    print(f'\nCUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    total_cost = 0
    valid_items = []  # List to store available items

    for item in c.shopping_list:
        # Check if the item is in the shop's stock
        stock_item = next((stock_item for stock_item in s.stock if stock_item.product.name == item.product.name), None)
        stock_quantity = getattr(stock_item, 'quantity', 0)
        
        if stock_item is not None and stock_quantity != 0:
            print_product(item.product)
            print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
            cost = int(item.quantity) * (item.product.price)
            c.cost += cost
            print(f'The cost to {c.name} will be €{round(cost,2):.2f}')
            
            valid_items.append(item)
        else:
            print(f"The item '{item.product.name}' is not available in the shop's stock, therefore no charge will be applied.")
        total_cost += cost
    c.shopping_list = valid_items  # Update shopping_list with valid items
    if total_cost <= c.budget:  # Check if the total cost is within the budget
        s.cash += total_cost  # Update shop's cash balance only if within budget
        print(f' \nThe total cost to {c.name} will be €{round(total_cost,2):.2f}')
    else:
        print(f"Error: {c.name}, total cost exceeds your budget.")

def main():
    print("Choose an option:")
    print("1. Input order using the live ordering system")
    print("2. Read the order from a CSV file")

    user_input = input("Enter your selection (1 or 2): ")

    if user_input == '1':
        s = create_and_stock_shop()
        c = read_customer_live_order(s)
        print_shop(s, c)
        print_customer(c, s)
        process_csv(c)
    elif user_input == '2':
        file_path = input("Enter the path to the CSV file: ")
        s = create_and_stock_shop()  
        c = read_customer_from_csv(file_path)
        print_shop(s, c)
        print_customer(c, s)
        process_csv(c)
    else:
        print("Invalid selection. Please enter 1 or 2.")

if __name__ == "__main__":
    main()

