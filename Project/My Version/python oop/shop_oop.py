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

    def create_and_stock_shop(self):
        with open('../shop.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.cash = float(next(csv_reader)[0])

        with open('../stock.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    product = Product(row[0], float(row[1]))
                    product_stock = ProductStock(product, int(row[2]))
                    self.stock.append(product_stock)
                except IndexError:
                    print()

    def print_shop(self, customer):
        print(f'\nShop has {self.cash} in opening cash')
        for item in self.stock:
            customer.print_product(item.product)
            print(f'The Shop has {item.quantity} of the above')
        customer.cost = sum(item.quantity * item.product.price for item in customer.shopping_list)

    def process_csv(self, customer, shop):
        with open('../shop.csv', 'r') as shopcsv:
            reader = csv.reader(shopcsv)
            data = [row for row in reader]

        self.cash = float(data[0][0])
        customer.cost = sum(item.quantity * item.product.price for item in customer.shopping_list)
        result = customer.perform_calculation(shop)
        data[0][0] = round(result, 2)
        print(f'\nAfter the above transaction, the Shop has a cash balance of: {result}')
        with open('../shop.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(data)


@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)
    cost: float = 0.0

    def read_customer_live_order(self, shop):
        print("Welcome to the shop!")
        self.name = input("Enter customer name: ")
        self.budget = float(input("Enter customer budget: "))

        while True:
            product_name = input("Shop Menu: Coke Can, Bread, Spaghetti, Tomato Sauce, Bin Bags, Jam, Bananas. Enter the product name (or 'done' to finish): ").strip().title()
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
            print(f'The cost for {quantity} {product_name}(s) will be €{round(cost):.2f}')

            if cost > self.budget:
                print(f"Error: {self.name}, you cannot afford this order.")
                continue

            confirm_order = input("Do you want to confirm the order? (y/n): ").lower()
            if confirm_order != 'y':
                print("Order canceled.")
                continue

            self.cost += cost
            self.budget -= cost
            shop.cash += cost

            stock_item.quantity -= quantity

            ps = ProductStock(stock_item.product, quantity)
            self.shopping_list.append(ps)

            print(f"Order confirmed. Remaining budget: €{round(self.budget):.2f}, would you like anything else?")
            print("")

    def read_customer_from_csv(self, file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])

            for row in csv_reader:
                name = row[0]
                customer_quantity = int(row[1])

                with open('../stock.csv') as stock_csv_file:
                    stock_csv_reader = csv.reader(stock_csv_file, delimiter=',')
                    stock_data = list(stock_csv_reader)

                stock_item = next((stock_row for stock_row in stock_data if stock_row[0] == name), None)

                if stock_item is not None:
                    stock_name = stock_item[0]
                    price = float(stock_item[1])
                    stock_quantity = int(stock_item[2])

                    if customer_quantity > stock_quantity:
                        print(f"Warning: Insufficient stock for {stock_name}. Requested: {customer_quantity}, Available: {stock_quantity}")

                    product = Product(name, price)
                    ps = ProductStock(product, customer_quantity)
                    self.shopping_list.append(ps)
                else:
                    print(f"Error: No stock information found for {name}")

    def print_product(self, product):
        print(f'\nPRODUCT NAME: {product.name} \nPRODUCT PRICE: {product.price}')

    def perform_calculation(self, shop):
        if self.cost <= self.budget:
            return shop.cash + self.cost
        else:
            return shop.cash

    def print_customer(self, shop):
        print(f'\nCUSTOMER NAME: {self.name} \nCUSTOMER BUDGET: {self.budget}')
        total_cost = 0
        valid_items = []

        for item in self.shopping_list:
            stock_item = next((stock_item for stock_item in shop.stock if stock_item.product.name == item.product.name), None)
            stock_quantity = getattr(stock_item, 'quantity', 0)

            if stock_item is not None and stock_quantity != 0:
                self.print_product(item.product)
                print(f'{self.name}ORDERS {item.quantity} OF ABOVE PRODUCT')
                cost = int(item.quantity) * round(item.product.price, 2)
                self.cost += cost
                print(f'The cost to {self.name} will be €{round(cost,2):.2f}')

                valid_items.append(item)
            else:
                print(f"The item '{item.product.name}' is not available in the shop's stock, therefore no charge will be applied.")
            total_cost += cost

        self.shopping_list = valid_items
        if total_cost <= self.budget:
            shop.cash += total_cost
            print(f' \nThe total cost to {self.name} will be € {round(total_cost,2):.2f}')
        else:
            print(f"Error: {self.name}, total cost exceeds your budget.")


def main():
    print("Choose an option:")
    print("1. Input order using the live ordering system")
    print("2. Read the order from a CSV file")

    user_input = input("Enter your selection (1 or 2): ")

    shop = Shop()
    customer = Customer()

    if user_input == '1':
        shop.create_and_stock_shop()
        customer.read_customer_live_order(shop)
        shop.print_shop(customer)
        customer.print_customer(shop)
        shop.process_csv(customer, shop)
    elif user_input == '2':
        file_path = input("Enter the path to the CSV file: ")
        shop.create_and_stock_shop()
        customer.read_customer_from_csv(file_path)
        shop.print_shop(customer)
        customer.print_customer(shop)
        shop.process_csv(customer, shop)
    else:
        print("Invalid selection. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
