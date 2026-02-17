import sys
# Use pyreadline3 on Windows when available, fall back to the builtin readline on Unix.
# This makes the module importable in CI (ubuntu) without requiring pyreadline3.
try:
    import pyreadline3 as readline
except Exception:
    try:
        import readline  # type: ignore
    except Exception:
        readline = None  # type: ignore

from typing import List
from app.calculation import Calculation, CalculationFactory


def display_help() -> None:
    
    help_message = """
Calculator REPL Help
--------------------
Usage:
    <operation> <number1> <number2>
    - Perform a calculation with the specified operation and two numbers.
    - Supported operations:
        add       : Adds two numbers.
        subtract  : Subtracts the second number from the first.
        multiply  : Multiplies two numbers.
        divide    : Divides the first number by the second.

Special Commands:
    help      : Display this help message.
    history   : Show the history of calculations.
    exit      : Exit the calculator.

Examples:
    add 10 5
    subtract 15.5 3.2
    multiply 7 8
    divide 20 4
    """
    print(help_message)


def display_history(history: List[Calculation]) -> None:
    """
    Displays the history of calculations performed during the session.

    Parameters:
        history (List[Calculation]): A list of Calculation objects representing past calculations.
    """
    if not history:
        print("No calculations performed yet.")
    else:
        print("Calculation History:")
        for idx, calculation in enumerate(history, start=1):
            print(f"{idx}. {calculation}")


def calculator() -> None:
    
    history: List[Calculation] = []

   
    print("Welcome to the Professional Calculator REPL!")
    print("Type 'help' for instructions or 'exit' to quit.\n")

   
    while True:
        try:
           
            user_input: str = input(">> ").strip()

            
            if not user_input:
                
                continue # pragma: no cover

            # Handle special commands
            command = user_input.lower()

            # LBYL is used here to check if the user input matches any special commands.
            if command == "help":
                display_help()
                continue
            elif command == "history":
                display_history(history)
                continue
            elif command == "exit":
                print("Exiting calculator. Goodbye!\n")
                sys.exit(0)  # Exit the program gracefully

            try:
                # Attempt to split the user input into operation and operands
                operation, num1_str, num2_str = user_input.split()
                # Convert the operand strings to floats
                num1: float = float(num1_str)
                num2: float = float(num2_str)
            except ValueError:
                print("Invalid input. Please follow the format: <operation> <num1> <num2>")
                print("Type 'help' for more information.\n")
                continue

            try:
                calculation = CalculationFactory.create_calculation(operation, num1, num2)
            except ValueError as ve:
                # Handle unsupported operations
                print(ve)
                print("Type 'help' to see the list of supported operations.\n")
                continue  # Prompt the user again

            # Attempt to execute the calculation
            try:
                result = calculation.execute()
            except ZeroDivisionError:
                # Handle division by zero specifically
                print("Cannot divide by zero.")
                print("Please enter a non-zero divisor.\n")
                continue  # Prompt the user again
            except Exception as e:
                # Handle any other unforeseen exceptions
                print(f"An error occurred during calculation: {e}")
                print("Please try again.\n")
                continue  # Prompt the user again

            # Prepare the result string for display
            result_str: str = f"{calculation}"
            print(f"Result: {result_str}\n")

            # Append the calculation object to history
            history.append(calculation)

        except KeyboardInterrupt:
            
            print("\nKeyboard interrupt detected. Exiting calculator. Goodbye!")
            sys.exit(0)
        except EOFError:
            
            print("\nEOF detected. Exiting calculator. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    calculator()  # pragma: no cover