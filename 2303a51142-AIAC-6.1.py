#  # Generate Python code to print all even numbers between 1 and N using a loop.
#  # Read the value of N from the user
# N = int(input("Enter a number: "))
# # Loop from 1 to N
# for i in range(1, N + 1):
#     # Check if the number is even
#     if i % 2 == 0:
#         print(i)

# print("\n")

# # Generate Python code to count how many numbers in a list are even and odd.
# def count_even_odd(numbers):
#     even_count = 0
#     odd_count = 0
    
#     # Loop through each number in the list
#     for num in numbers:
#         # Check if the number is even or odd
#         if num % 2 == 0:
#             even_count += 1  # Increment even count
#         else:
#             odd_count += 1   # Increment odd count
    
#     return even_count, odd_count
# # Sample test
# numbers = [10, 15, 22, 33, 42, 55, 60, 71, 80, 91, 100]
# even_count, odd_count = count_even_odd(numbers)
# print(f"Even numbers: {even_count}, Odd numbers: {odd_count}")


# print("\n")



# #Generate a Python class User that validates age and email using conditional statements.
# class User:
#     # Constructor to initialize age and email
#     def __init__(self, age, email):
#         self.age = age
#         self.email = email

#     # Validate age (must be 18 or above)
#     def validate_age(self):
#         return self.age >= 18

#     # Validate email format
#     def validate_email(self):
#         return "@" in self.email and "." in self.email


# # Create user objects for testing
# user1 = User(20, "test@example.com")
# user2 = User(15, "invalidemail")

# # Display validation results
# print(user1.validate_age(), user1.validate_email())
# print(user2.validate_age(), user2.validate_email())

# print("\n")




# #Generate a Python class Student with attributes (name, roll number, marks) and methods to calculate total and average marks.

# class Student:
#     # Constructor to initialize name, roll number, and marks
#     def __init__(self, name, roll_number, marks):
#         self.name = name
#         self.roll_number = roll_number
#         self.marks = marks  # marks should be a list of integers

#     # Method to calculate total marks
#     def total_marks(self):
#         return sum(self.marks)

#     # Method to calculate average marks
#     def average_marks(self):
#         if len(self.marks) == 0:
#             return 0
#         return self.total_marks() / len(self.marks)
# # Create student objects for testing
# student1 = Student("Vikas", 101, [85, 90, 78])
# student2 = Student("Sai", 102, [88, 76, 92, 85])
# # Display total and average marks
# print(f"{student1.name} - Total: {student1.total_marks()}, Average: {student1.average_marks()}")
# print(f"{student2.name} - Total: {student2.total_marks()}, Average: {student2.average_marks()}")

# print("\n")


# #Generate a Python program for a simple bank account system using class, loops, and conditional statements.

# class BankAccount:
#     # Constructor to initialize account holder name and balance
#     def __init__(self, account_holder, initial_balance=0):
#         self.account_holder = account_holder
#         self.balance = initial_balance

#     # Method to deposit money
#     def deposit(self, amount):
#         if amount > 0:
#             self.balance += amount
#             print(f"Deposited: {amount}. New Balance: {self.balance}")
#         else:
#             print("Deposit amount must be positive.")

#     # Method to withdraw money
#     def withdraw(self, amount):
#         if amount > 0:
#             if amount <= self.balance:
#                 self.balance -= amount
#                 print(f"Withdrew: {amount}. New Balance: {self.balance}")
#             else:
#                 print("Insufficient balance.")
#         else:
#             print("Withdrawal amount must be positive.")

#     # Method to display current balance
#     def display_balance(self):
#         print(f"Current Balance: {self.balance}")   
# # Create a bank account object for testing
# account = BankAccount("Rohith", 500)
# # Perform some transactions
# account.display_balance()
# account.deposit(200)
# account.withdraw(100)
# account.withdraw(700)
# account.display_balance()

# print("\n")



# # # a supermarket wants to automate its monthly sales analysis syaystem. using a python program to help the manager understand product-wise and day-wise sales performance. you are required to develop a console based application that uses multiple loops for process sales data the program should should first ask for the number of days in the month and then for each day ask the number of product sold using a nested loop structure the program shlould accept thr name of each product and the quality sold on the day the program must calculate the total quality sold for each product accroess all the dats and also copute the overall sales quality for the entire month after proccessing all inputs the program should display a clear sumarry howing day-wise sales, product-wise totals, ans the grand total sales fir thr month the system dhould allow the manager repeat the anslusus for another month if required 

# # # Supermarket Monthly Sales Analysis System

# # # This loop allows the manager to repeat the analysis for another month
while True:
    # Dictionary to store total quantity sold for each product across all days
    product_totals = {}

    # Dictionary to store day-wise sales details
    day_wise_sales = {}

    # Variable to store overall sales quantity for the month
    grand_total = 0

    # Input number of days in the month
    days = int(input("\nEnter number of days in the month: "))

    # Loop for each day
    for day in range(1, days + 1):
        print(f"\nDay {day} Sales Entry")
        day_wise_sales[day] = []

        # Input number of products sold on this day
        products_count = int(input("Enter number of products sold today: "))

        # Nested loop for each product
        for _ in range(products_count):
            # Input product name and quantity sold
            product_name = input("Enter product name: ")
            quantity = int(input("Enter quantity sold: "))

            # Store day-wise sales
            day_wise_sales[day].append((product_name, quantity))

            # Update product-wise totals
            if product_name in product_totals:
                product_totals[product_name] += quantity
            else:
                product_totals[product_name] = quantity

            # Update grand total
            grand_total += quantity

    # Display summary report
    print("\n========== Monthly Sales Summary ==========")

    # Day-wise sales summary
    print("\nDay-wise Sales:")
    for day, sales in day_wise_sales.items():
        print(f"Day {day}:")
        for product, qty in sales:
            print(f"  {product} - {qty}")

    # Product-wise total sales
    print("\nProduct-wise Total Sales:")
    for product, total in product_totals.items():
        print(f"{product}: {total}")

    # Grand total sales
    print(f"\nGrand Total Sales for the Month: {grand_total}")

    # Ask if manager wants to repeat analysis
    choice = input("\nDo you want to analyze another month? (yes/no): ").lower()
    if choice != "yes":
        print("Exiting Sales Analysis System.")
        break
