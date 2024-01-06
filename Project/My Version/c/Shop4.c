#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_PRODUCTS 10
#define MAX_NAME_LENGTH 50

struct Product {
    char name[MAX_NAME_LENGTH];
    double price;
};

struct ProductStock {
    struct Product product;
    int quantity;
};

struct Shop {
    double cash;
    struct ProductStock stock[MAX_PRODUCTS];
    int index;
};

struct Customer {
    char name[MAX_NAME_LENGTH];
    float budget;
    float initialBudget;
    struct ProductStock shoppingList[MAX_PRODUCTS];
    float cost;
    int index;
};

struct Shop createAndStockShop() {
    FILE *shopFile, *stockFile;
    char shopLine[256], stockLine[256];
    float cash;

    // Open shop.csv for reading cash value
    shopFile = fopen("shop.csv", "r");
    if (shopFile == NULL)
        exit(EXIT_FAILURE);

    // Read the cash value
    if (fgets(shopLine, sizeof(shopLine), shopFile) != NULL) {
        sscanf(shopLine, "%f", &cash);
    } else {
        printf("Error reading cash from shop.csv\n");
        exit(EXIT_FAILURE);
    }

    struct Shop shop = {cash};
    shop.index = 0; // Reset the index to zero

    fclose(shopFile);

    // Open stock.csv for reading product information
    stockFile = fopen("stock.csv", "r");
    if (stockFile == NULL)
        exit(EXIT_FAILURE);

    // Read product information
    while (fgets(stockLine, sizeof(stockLine), stockFile) != NULL) {
        // Parse the line to extract product information
        char *token = strtok(stockLine, ",");
        if (token == NULL) {
            printf("Error: Malformed line in stock.csv\n");
            continue;
        }

        // Extract product name
        strcpy(shop.stock[shop.index].product.name, token);

        // Extract product price
        token = strtok(NULL, ",");
        if (token == NULL) {
            printf("Error: Malformed line in stock.csv\n");
            continue;
        }
        shop.stock[shop.index].product.price = atof(token);

        // Extract quantity
        token = strtok(NULL, ",");
        if (token == NULL) {
            printf("Error: Malformed line in stock.csv\n");
            continue;
        }
        shop.stock[shop.index].quantity = atoi(token);

        // Move to the next index
        shop.index++;

        // Check if we have read the maximum number of products
        if (shop.index >= MAX_PRODUCTS) {
            printf("Warning: Maximum number of products reached\n");
            break;
        }
    }

    fclose(stockFile);

    return shop;
}

// Function to convert a string to lowercase.
void toLowerCase(char *str) {
    for (int i = 0; str[i]; i++) {
        // Convert alphabetic characters to lowercase
        if (isalpha((unsigned char)str[i])) {
            str[i] = tolower((unsigned char)str[i]);
        }
        // Convert spaces to lowercase
        else if (str[i] == ' ') {
            str[i] = tolower((unsigned char)str[i]);
        }
    }
}

// Function to capitalize the first letter of each word.
void capitalizeFirstLetter(char *str) {
    int i = 0;
    int capitalized = 0; // Flag to check if the first letter is capitalized

    while (str[i]) {
        if (i == 0 || (i > 0 && str[i-1] == ' ')) {
            // Capitalize the first letter of the word
            str[i] = toupper((unsigned char)str[i]);
            capitalized = 1;
        } else if (capitalized && isalpha((unsigned char)str[i])) {
            // Make other letters of the word lowercase
            str[i] = tolower((unsigned char)str[i]);
        }
        i++;
    }
}


// Function to calculate the total cost of the customer order.
void calculateTotalCost(struct Customer *customer) {
    float totalCost = 0.0;

    for (int i = 0; i < customer->index; i++) {
        totalCost += customer->shoppingList[i].quantity * customer->shoppingList[i].product.price;
    }

    customer->cost = totalCost;
}

// Calculates the cost of a specific product stock.
float calculateProductCost(struct ProductStock *productStock) {
    return productStock->quantity * productStock->product.price;
}

// Function to print the product's details.
void printProduct(struct Product product) {
    capitalizeFirstLetter(product.name); // Capitalize the product name before printing
    printf("\nPRODUCT NAME: %s \nPRODUCT PRICE: €%.2f\n", product.name, product.price);
}

// Function to print the shop info.
void printShop(struct Shop *shop) {
    printf("\nShop has €%.2f in opening cash\n", shop->cash);
    for (int i = 0; i < shop->index; i++) {
        if (strlen(shop->stock[i].product.name) > 0) {
            printProduct(shop->stock[i].product);
            printf("The Shop has %d of the above\n", shop->stock[i].quantity);
        }
    }
}

// Function that processes the customer's order using the live ordering system.
void processOrder(struct Shop *shop, struct Customer *customer) {
    char product_name[MAX_NAME_LENGTH];
    int quantity;

    while (1) {
        printf("Shop Menu: Coke Can, Bread, Spaghetti, Tomato Sauce, Bin Bags, Jam, Bananas. Enter the product name (or 'done' to finish): ");
        scanf(" %[^\n]", product_name);  // Read the entire line, including spaces

        if (strcmp(product_name, "done") == 0) {
            break;
        }

        int found = 0;

        for (int i = 0; i < MAX_PRODUCTS && !found; i++) {
            char temp[MAX_NAME_LENGTH];
            int j;

            for (j = 0; shop->stock[i].product.name[j]; j++) {
                temp[j] = tolower(shop->stock[i].product.name[j]);
            }
            temp[j] = '\0';

            // Use strstr to check if the product_name is a substring of the temp
            if (strstr(temp, product_name) != NULL) {
                found = 1;
                printf("Enter the quantity of %s: ", shop->stock[i].product.name);
                scanf("%d", &quantity);

                if (quantity <= 0) {
                    printf("Error: Quantity should be a positive integer.\n");
                    continue;
                }

                if (quantity > shop->stock[i].quantity) {
                    printf("\n Error: The item %s is not available in the shop's stock, therefore no charge will be applied.  %d\n", shop->stock[i].product.name, shop->stock[i].quantity);
                    continue;
                }

                float cost = quantity * shop->stock[i].product.price;
                printf("The cost for %d %s(s) will be €%.2f\n", quantity, shop->stock[i].product.name, cost);

                if (cost > customer->budget) {
                    printf("Error: %s, you cannot afford this order.\n", customer->name);
                    continue;
                }

                char confirm_order;
                printf("Do you want to confirm the order? (y/n): ");
                scanf(" %c", &confirm_order);

                if (confirm_order != 'y') {
                    printf("Order canceled.\n");
                    continue;
                }
                customer->shoppingList[customer->index].product = shop->stock[i].product;
                customer->shoppingList[customer->index].quantity = quantity;
                customer->index++;
                customer->cost += cost;
                customer->budget -= cost;
                shop->cash += cost;

                shop->stock[i].quantity -= quantity;

                printf("Order confirmed. Remaining budget: €%.2f, would you like anything else?\n", customer->budget);
            }
        }

        if (!found) {
            printf("Error: No stock information found for '%s'\n", product_name);
        }
    }
}
// Function that process the customer's order when placed through a csv file.
void processOrderCSV(struct Shop *shop, struct Customer *customer, const char *file_path) {
    FILE *orderFile = fopen(file_path, "r");
    if (orderFile == NULL) {
        printf("Error: Unable to open file %s\n", file_path);
        return;
    }

    char line[100];
    int lineCount = 0;
    float totalCost = 0.0;

    // Read and print each product order with cost
    while (fgets(line, sizeof(line), orderFile)) {
        line[strcspn(line, "\n")] = 0; // Remove newline character

        if (lineCount == 0) {
            // First line: Customer name and budget
            sscanf(line, "%49[^,], €%f", customer->name, &customer->budget);
        } else {
            // Subsequent lines: Product name and quantity
            char productName[MAX_NAME_LENGTH];
            int quantity;
            sscanf(line, "%49[^,], %d", productName, &quantity);

            int found = 0;
            for (int i = 0; i < shop->index; i++) {
                if (strcasecmp(shop->stock[i].product.name, productName) == 0) {
                    found = 1;
                    float cost = quantity * shop->stock[i].product.price;
                    totalCost += cost;

                    printf("PRODUCT NAME: %s\n", shop->stock[i].product.name);
                    printf("PRODUCT PRICE: €%.2f\n", shop->stock[i].product.price);
                    printf("%s ORDERS %d OF ABOVE PRODUCT\n", customer->name, quantity);
                    printf("The cost to %s will be €%.2f\n\n", customer->name, cost);

                    break;
                }
            }
            if (!found) {
                printf("Error: No stock information found for '%s'\n", productName);
            }
        }
        lineCount++;
    }

    // Check if total cost exceeds budget
    if (totalCost > customer->budget) {
        printf("\nError: %s total cost exceeds your budget.\n", customer->name);
        fclose(orderFile);
        return;
    }

    // Rewind the file for the second pass
    rewind(orderFile);
    lineCount = 0; // Reset line count for the second pass

    // Second pass to process each product
    while (fgets(line, sizeof(line), orderFile)) {
        line[strcspn(line, "\n")] = 0; // Remove newline character

        if (lineCount > 0) { // Skip the first line (customer info)
            char productName[MAX_NAME_LENGTH];
            int quantity;
            sscanf(line, "%49[^,], %d", productName, &quantity);

            for (int i = 0; i < shop->index; i++) {
                if (strcasecmp(shop->stock[i].product.name, productName) == 0) {
                    if (quantity <= shop->stock[i].quantity) {
                        float cost = quantity * shop->stock[i].product.price;
                        customer->budget -= cost;
                        shop->cash += cost;
                        shop->stock[i].quantity -= quantity;
                        customer->shoppingList[customer->index].product = shop->stock[i].product;
                        customer->shoppingList[customer->index].quantity = quantity;
                        customer->index++;
                    } else {
                        printf("Error: The item %s is not available in the shop's stock, therefore no charge will be applied. \n", productName);
                    }
                    break;
                }
            }
        }
        lineCount++;
    }

    fclose(orderFile);
}

// Function that prints the final status of the customer's order.
void printCustomer(struct Shop *shop, struct Customer customer) {
    calculateTotalCost(&customer);
    printf("\nCUSTOMER NAME: %s\n", customer.name);
    printf("CUSTOMER BUDGET: %.2f\n", customer.initialBudget);

    for (int i = 0; i < customer.index; i++) {
        printProduct(customer.shoppingList[i].product);
        float productCost = calculateProductCost(&customer.shoppingList[i]);
        printf("%s ORDERS %d OF THE ABOVE PRODUCT\n", customer.name, customer.shoppingList[i].quantity);
        printf("The cost to %s will be €%.2f\n", customer.name, productCost);
    }

    printf("\nThe total cost to %s is €%.2f\n", customer.name, customer.cost);

    float result = customer.cost <= customer.budget ? shop->cash + customer.cost : shop->cash;
    printf("\nAfter the above transaction, the Shop has a cash balance of: €%.2f\n", result);

    // Update the cash balance in the shop
    shop->cash = result;
}

// Function that processes the shop and customer details from a csv file.
void processCSV(struct Shop *shop, struct Customer *customer) {
    FILE *shopCSV = fopen("shop.csv", "r");
    if (shopCSV != NULL) {
        if (fscanf(shopCSV, "%lf", &shop->cash) != 1) {
            printf("Error reading cash from shop.csv\n");
            fclose(shopCSV);
            return;
        }
        fclose(shopCSV);
    } else {
        printf("Error opening shop.csv\n");
        return;
    }


    FILE *stockCSV = fopen("stock.csv", "r");
    if (stockCSV != NULL) {
        char line[220];
        for (int i = 0; i < MAX_PRODUCTS && fgets(line, sizeof(line), stockCSV); i++) {
            if (sscanf(line, " %49[^,], %lf, %d", shop->stock[i].product.name, &shop->stock[i].product.price, &shop->stock[i].quantity) != 3) {
                printf("Error reading stock data from stock.csv\n");
                continue;
            }
        }
        fclose(stockCSV);
    } else {
        printf("Error opening stock.csv\n");
        return;
    }

    FILE *outfile = fopen("shop.csv", "w");
    if (outfile != NULL) {
        fprintf(outfile, "%.2f", shop->cash);
        fclose(outfile);
    } else {
        printf("Error opening shop.csv for writing\n");
    }
}

// Function that reads customer's live order details.
void readCustomerLiveOrder(struct Shop *shop, struct Customer *customer) {
    printf("Welcome to the shop!\n");
    printf("Enter customer name: ");
    scanf("%s", customer->name);

    printf("Enter customer budget: ");
    scanf("%f", &customer->budget);
    customer->initialBudget = customer->budget;
}

// Function to read customer information from a csv file.
void customerReadFromCSV(struct Customer *customer, const char *file_path) {
    FILE *customerCSV = fopen(file_path, "r");
    if (customerCSV == NULL) {
        printf("Error: Unable to open file %s\n", file_path);
        return;
    }

    if (fscanf(customerCSV, "%49[^,], %f", customer->name, &customer->budget) != 2) {
        printf("Error: Incorrect format or incomplete data in %s\n", file_path);
    } else {
        printf("Customer data read successfully from %s\n", file_path);
    }

    fclose(customerCSV);
    customer->initialBudget = customer->budget;
}

// Main function to run the program.
int main() {
    struct Shop shop = createAndStockShop();
    struct Customer customer = {"", 0.0};

    printf("Choose an option:\n");
    printf("1. Input order using the live ordering system\n");
    printf("2. Read the order from a CSV file\n");

    char user_input;
    printf("Enter your selection (1 or 2): ");
    scanf(" %c", &user_input);

    if (user_input == '1') {
        readCustomerLiveOrder(&shop, &customer);
        processOrder(&shop, &customer);
        processCSV(&shop, &customer);
        printShop(&shop);
        printCustomer(&shop, customer);
    } else if (user_input == '2') {
        char file_path[100];
        printf("Enter the path to the CSV file: ");
        scanf("%s", file_path);
        customerReadFromCSV(&customer, file_path);
        printShop(&shop);
        processCSV(&shop, &customer);
        processOrderCSV(&shop, &customer, file_path);
        printCustomer(&shop, customer);
    } else {
        printf("Invalid selection. Please enter 1 or 2.\n");
    }

    return 0;
}
