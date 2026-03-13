"""
Professional Simple Calculator (Enhanced)
------------------------------------------
Prompts the user for two numbers and an arithmetic operation.
Supports: addition (+), subtraction (-), multiplication (*), division (/),
          modulus (%), exponentiation (**), floor division (//).
Includes input validation, error handling, and multiple calculations.
"""

def get_number(prompt):
    """Prompt for a number and return it as a float. Re-prompt on invalid input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_operation():
    """Prompt for an arithmetic operation and return it. Re-prompt if invalid."""
    valid_ops = ['+', '-', '*', '/', '%', '**', '//']
    while True:
        op = input("Enter operation (+, -, *, /, %, **, //): ").strip()
        if op in valid_ops:
            return op
        print("Invalid operation. Please choose from +, -, *, /, %, **, //.")

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError("Modulus by zero is not allowed.")
    return a % b

def power(a, b):
    return a ** b

def floor_divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Floor division by zero is not allowed.")
    return a // b

def calculate(num1, num2, op):
    """Perform the calculation by calling the appropriate function."""
    try:
        if op == '+':
            return add(num1, num2)
        elif op == '-':
            return subtract(num1, num2)
        elif op == '*':
            return multiply(num1, num2)
        elif op == '/':
            return divide(num1, num2)
        elif op == '%':
            return modulus(num1, num2)
        elif op == '**':
            return power(num1, num2)
        elif op == '//':
            return floor_divide(num1, num2)
    except ZeroDivisionError as e:
        return f"Error: {e}"
    except OverflowError:
        return "Error: Result too large to compute."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    print("=" * 50)
    print("          PROFESSIONAL CALCULATOR (ENHANCED)")
    print("=" * 50)

    while True:
        print("\n--- New Calculation ---")
        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")
        op = get_operation()

        result = calculate(num1, num2, op)

        print("\n" + "-" * 30)
        print(f"Result: {num1} {op} {num2} = {result}")
        print("-" * 30)

        again = input("\nDo you want to perform another calculation? (yes/no): ").strip().lower()
        if again not in ['yes', 'y']:
            print("\nThank you for using the Professional Calculator. Goodbye!")
            break

if __name__ == "__main__":
    main()
    
