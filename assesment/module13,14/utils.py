import datetime
import os

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, required=True):
    """Gets input from user and validates it if required."""
    while True:
        value = input(prompt).strip()
        if required and not value:
            print("\033[91mError: This field cannot be empty. Please try again.\033[0m")
            continue
        return value

def get_date():
    """Asks user for date or generates it automatically."""
    print("\nDate Selection:")
    print("1. Auto-generate (Today)")
    print("2. Enter manually")
    choice = input("Select an option (1/2) [Default 1]: ").strip()
    
    if choice == '2':
        return get_input("Enter date (DD-MM-YYYY): ")
    else:
        return datetime.datetime.now().strftime("%d-%b-%Y %H:%M")

def print_header(title):
    """Prints a styled header."""
    width = 50
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)

def print_message(message, type="info"):
    """Prints a styled message."""
    colors = {
        "info": "\033[94m",    # Blue
        "success": "\033[92m", # Green
        "error": "\033[91m",   # Red
        "warning": "\033[93m", # Yellow
        "reset": "\033[0m"
    }
    print(f"{colors.get(type, colors['info'])}{message}{colors['reset']}")
