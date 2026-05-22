import sys
from utils import clear_screen, print_header, print_message
import auth
import posts

def main_menu():
    """Main menu after login."""
    while True:
        print_header("PostBoard - Employee Dashboard")
        print("1. Create a Post")
        print("2. View All Posts")
        print("3. Search Posts by Username")
        print("4. Logout")
        print("5. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            posts.create_post(current_user)
        elif choice == '2':
            posts.view_all_posts()
        elif choice == '3':
            posts.search_posts_by_username()
        elif choice == '4':
            print_message("Logging out...", "info")
            break
        elif choice == '5':
            print_message("Goodbye!", "success")
            sys.exit()
        else:
            print_message("Invalid choice. Please try again.", "error")
        
        input("\nPress Enter to continue...")
        clear_screen()

def landing_page():
    """Landing page for login/register."""
    global current_user
    while True:
        clear_screen()
        print_header("Welcome to PostBoard")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == '1':
            user = auth.login()
            if user:
                current_user = user
                clear_screen()
                main_menu()
        elif choice == '2':
            auth.register()
            input("\nPress Enter to continue...")
        elif choice == '3':
            print_message("Goodbye!", "success")
            sys.exit()
        else:
            print_message("Invalid choice. Please try again.", "error")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    current_user = None
    landing_page()
