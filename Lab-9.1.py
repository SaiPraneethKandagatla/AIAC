"""Lab 9.1 — Documentation Styles Example.

Problem:
		Document a simple utility function that returns the maximum value in a
		sequence of numbers, using multiple documentation approaches.
"""
def find_max_docstring(numbers):
		"""Return the maximum value from a non-empty iterable of numbers.

		Parameters
		----------
		numbers : iterable
				A non-empty iterable containing numeric values.

		Returns
		-------
		number
				The largest value in the input.

		Raises
		------
		ValueError
				If `numbers` is empty.
		TypeError
				If the values in `numbers` cannot be compared.
		"""

		return max(numbers)

def find_max_inline_comments(numbers):
		# Purpose: return the largest element of a non-empty iterable.
		# Note: Python's built-in max() raises ValueError on empty input.

		# Delegate to the built-in implementation (efficient and well-tested).
		maximum_value = max(numbers)

		# Return the computed maximum to the caller.
		return maximum_value

def find_max_google(numbers):
		"""Returns the maximum value from a non-empty iterable of numbers.

		Args:
				numbers: A non-empty iterable of numeric values.

		Returns:
				The largest value present in `numbers`.

		Raises:
				ValueError: If `numbers` is empty.
				TypeError: If elements in `numbers` are not comparable.

		Examples:
				>>> find_max_google([1, 5, 2])
				5
				>>> find_max_google((-3, -7, 0))
				0
		"""

		return max(numbers)

if __name__ == "__main__":
	raw = input("Enter numbers separated by space or comma: ").strip()
	if not raw:
		raise ValueError("No numbers entered.")

	tokens = raw.replace(",", " ").split()
	values = []
	for token in tokens:
		number = float(token)
		values.append(int(number) if number.is_integer() else number)

	print("Input:", values)
	print("Max (docstring):", find_max_docstring(values))
	print("Max (inline comments):", find_max_inline_comments(values))
	print("Max (Google-style):", find_max_google(values))


# TASK 2:
def login(user, password, credentials):
    """
    Validates user login credentials.

    Args:
        user (str): Username entered by the user.
        password (str): Password entered by the user.
        credentials (dict): Dictionary containing usernames
                            as keys and passwords as values.

    Returns:
        bool: Returns True if login is successful,
              otherwise False.
    """
    return credentials.get(user) == password
credentials = {}

n = int(input("Enter number of users: "))

for i in range(n):
    print(f"\nEnter details for User {i+1}")
    username = input("Username: ")
    password = input("Password: ")
    credentials[username] = password

print("\n----- LOGIN -----")

login_user = input("Enter username: ")
login_password = input("Enter password: ")
if login(login_user, login_password, credentials):
    print("Login Successful")
else:
    print("Invalid Username or Password")


#TASK 3:
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
if __name__ == "__main__":

    print("\n===== SIMPLE CALCULATOR =====")

    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    print("\n1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter choice: ")

    if choice == '1':
        print("Result:", add(a, b))

    elif choice == '2':
        print("Result:", subtract(a, b))

    elif choice == '3':
        print("Result:", multiply(a, b))

    elif choice == '4':
        try:
            print("Result:", divide(a, b))
        except ValueError as e:
            print(e)
    else:
        print("Invalid Choice")