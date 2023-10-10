#author Emma Dunleavy
#MPP Week 1 Programming Exercises

#Write a program that asks the user for their name and greets them with their name.

name = input("What is your name? ")
print("Hi" , name)

#Modify the previous program such that only the users Alice and Bob are greeted with their names.

name = input("What is your name? ")

if name == "Alice":
    print("Hi" , name)
elif name == "Bob":
    print("Hi" , name)
else:
    print()

#Write a program that asks the user for a number n and prints the sum of the numbers 1 to n

n = int(input("Please enter an iteger "))

sum = 0
for i in range (1, n+1):
    sum += i
print(sum)

#Modify the previous program such that only multiples of three or five are considered in the sum, e.g.
# 3, 5, 6, 9, 10, 12, 15 for n=17

n = int(input("Please enter an iteger "))

sum = 0
for i in range (1, n+1):
     if i%3 == 0 or i%5 == 0:  # % divid by and rmainder is equal to... (modulus)
        sum += i
print(sum)


# Write a program that asks the user for a number n and gives them the possibility to choose between computing the sum and computing the product of 1,. . . ,n.
n = int(input("Please enter an iteger "))
option = int(input("Please enter 1 for product, enter 2 for sum "))
          
product = 1 
sum = 0 
if option == 1 : 
    for number in range(1, n+1): 
        product *= number 
    print("Product of the inputted number ", n, "is", product) 
    
elif option == 2: 
    for number in range(1, n+1): 
        sum += number 
    print("Sum of numbers up to ", n, "is", sum)        

else:  
    print("Please enter either 1 or 2") 


# Write a program that prints a multiplication table for numbers up to 12.

num = int(input("Please enter an iteger "))

# Iterate 12 times from i = 1 to 12
for i in range(1, 13):
   print(num, 'x', i, '=', num*i)

# Write a program that prints all prime numbers smaller than 100.

def checkPrime(num):

    #  0, 1 and negative numbers are not prime
    if num < 2:
        return 0
    else:

        # no need to run loop till num-1 as for any number x the numbers in
        # the range(num/2 + 1, num) won't be divisible anyway
        #// divids by and rounds to the nearest number
        x = num // 2
        for j in range(2, x + 1):
            if num % j == 0:
                return 0

    # the number would be prime if we reach here
    return 1


for i in range(1, 100 + 1):
    if checkPrime(i):
        print(i, end=" ")