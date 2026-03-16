#Task Description 1: Classes (Student Class)

#Generate a Python class Student with attributes (name, roll number, marks).

class Student:
    def __init__(self, name, roll_number, branch):
        self.name = name
        self.roll_number = roll_number
        self.branch = branch

    def display_details(self):
        print("Student Details:")
        print(f"Name       : {self.name}")
        print(f"Roll No    : {self.roll_number}")
        print(f"Branch     : {self.branch}")


# Sample object creation
student1 = Student("Ravi Kumar", "21CSE045", "Computer Science Engineering")
student2 = Student("Sai", "21CSE046", "Civil Engineering")
student3 = Student("Anita", "21CSE047", "Computer Science Engineering")
student4 = Student("Vikas", "21CSE048", "Electronics Engineering")

# Display student information
student1.display_details()
student2.display_details()
student3.display_details()
student4.display_details()
print("\n")


#Task Description 2: Loops (Multiples of a Number)

#You are writing a utility function to display multiples of a given number. Task is to create a function that takes a number and prints its multiples up to a specified limit using loops.
def print_multiples(number, limit):
    print(f"Multiples of {number} up to {limit}:")
    for i in range(1, limit + 1):
        multiple = number * i
        print(multiple, end=' ')
    print()
# Sample function call
print_multiples(7, 10)
print_multiples(2, 10)
print_multiples(5, 10)
print_multiples(2, 10)


print("\n")

#Task Description 3: Conditional Statements (Age Classification)

#You are building a basic classification system based on age.
def classify_age(age):
    if age < 0:
        return "Invalid age"
    elif age <= 12:
        return "Child"
    elif age <= 19:
        return "Teenager"
    elif age <= 59:
        return "Adult"
    else:
        return "Senior Citizen"
# Sample function calls
ages = [10, 15, 25, 65, -5]
for age in ages:
    classification = classify_age(age)
    print(f"Age: {age}, Classification: {classification}")
print("\n")



#Task Description 4: For and While Loops (Sum of First n Numbers)

#You need to calculate the sum of the first n natural numbers.
def sum_of_n_numbers(n):
    # Using for loop
    sum_for = 0
    for i in range(1, n + 1):
        sum_for += i

    # Using while loop
    sum_while = 0
    count = 1
    while count <= n:
        sum_while += count
        count += 1

    return sum_for, sum_while
# Sample function call
n = 10
sum_for, sum_while = sum_of_n_numbers(n)
print(f"Sum of first {n} natural numbers using for loop: {sum_for}")
print(f"Sum of first {n} natural numbers using while loop: {sum_while}")
print("\n")


#Task Description 5: Classes (Bank Account Class)

#You are designing a basic banking application.
class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}. New Balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew: {amount}. New Balance: {self.balance}")
        else:
            print("Insufficient balance or invalid withdrawal amount.")

    def display_balance(self):
        print(f"Account Holder: {self.account_holder}, Balance: {self.balance}")
# Sample object creation and operations
account = BankAccount("Ravi Kumar", 1000)
account.display_balance()
account.deposit(500)
account.withdraw(300)
account.withdraw(1500)
account.display_balance()
print("\n")