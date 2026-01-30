# Task 1: Zero-Shot Prompting – Leap Year Check
def is_leap_year(year):
    # Check if the year is divisible by 400
    # OR divisible by 4 but not divisible by 100
    if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
        return True  # It is a leap year
    return False     # It is not a leap year


# Sample test cases
print(is_leap_year(2024))  # Expected Output: True
print(is_leap_year(2023))  # Expected Output: False
print(is_leap_year(2000))  # Expected Output: True
print(is_leap_year(1900))  # Expected Output: False
print(is_leap_year(1600))  # Expected Output: True




# Task 2: One-Shot Prompting – Centimeters to Inches Conversion
def cm_to_inches(cm):
    # Convert centimeters to inches using the formula:
    # 1 inch = 2.54 centimeters
    return cm / 2.54

# Sample test cases
print(cm_to_inches(10))   # Expected Output: 3.94
print(cm_to_inches(25))   # Expected Output: 9.84
print(cm_to_inches(0))    # Expected Output: 0.0
print(cm_to_inches(100))  # Expected Output: 39.37



# Task 3: Few-Shot Prompting – Name Formatting
def format_name(full_name):
    # Split the full name into parts based on spaces
    parts = full_name.split()
    
    # First word is considered as first name
    first_name = parts[0]
    
    # Last word is considered as last name
    last_name = parts[-1]
    
    # Return the name in "Last, First" format
    return f"{last_name}, {first_name}"


# Sample test cases
print(format_name("Ellipai Rohith"))   # Expected Output: Rohith, Ellipai
print(format_name("Anita Rao"))    # Expected Output: Rao, Anita
print(format_name("Katkar Sanskar"))  # Expected Output: Sanskar, Katkar
print(format_name("Musham Vikas"))   # Expected Output: Vikas, Musham
print(format_name("Sai Praneeth Kandagatla")) # Expected Output: Kandagatla, Sai Praneeth



# Task 4: Comparative Analysis – Zero-Shot vs Few-Shot

# Comparative Analysis – Zero-Shot
def count_vowels_zero_shot(text):
    # Define all vowels (both lowercase and uppercase)
    vowels = "aeiouAEIOU"
    count = 0
    
    # Loop through each character in the string
    for char in text:
        # Check if the character is a vowel
        if char in vowels:
            count += 1  # Increment count if vowel found
    
    # Return total vowel count
    return count


# Sample test
print(count_vowels_zero_shot("Hello World"))  # Expected Output: 3
print(count_vowels_zero_shot("AI is amazing!"))  # Expected Output: 6
print(count_vowels_zero_shot("Python Programming"))  # Expected Output: 4
print(count_vowels_zero_shot("Data Science"))  # Expected Output: 5

# Comparative Analysis –  Few-Shot
def count_vowels_few_shot(text):
    # Convert text to lowercase for uniform comparison
    text = text.lower()
    
    # Count vowels using a generator expression
    return sum(1 for char in text if char in "aeiou")


# Sample test
print(count_vowels_few_shot("Hello World"))  # Expected Output: 3
print(count_vowels_few_shot("AI is amazing!"))  # Expected Output: 6
print(count_vowels_few_shot("Python Programming"))  # Expected Output: 4
print(count_vowels_few_shot("Data Science"))  # Expected Output: 5









# Task 5: Few-Shot Prompting – File Handling  
def count_lines(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Count each line using a generator expression
        line_count = sum(1 for line in file)
    
    # Return the total number of lines
    return line_count


# Sample test
print(count_lines("example.txt"))  # Expected Output: 3