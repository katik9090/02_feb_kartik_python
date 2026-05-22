from utils import get_input, print_message

# In-memory user storage: {username: password}
users = {}

def register():
    """Handles user registration."""
    print("\n--- Register ---")
    username = get_input("Enter a new username: ")
    
    if username in users:
        print_message("Error: Username already exists. Please try another.", "error")
        return None
    
    password = get_input("Enter a password: ")
    users[username] = password
    print_message("Registration successful! You can now log in.", "success")
    return username

def login():
    """Handles user login."""
    print("\n--- Login ---")
    username = get_input("Username: ")
    password = get_input("Password: ")
    
    if username in users and users[username] == password:
        print_message(f"Welcome back, {username}!", "success")
        return username
    else:
        print_message("Invalid username or password.", "error")
        return None
