from utils import get_input, get_date, print_message, print_header

# In-memory post storage: list of dictionaries
posts = []

def create_post(author):
    """Creates a new post and adds it to the storage."""
    print_header("Create New Post")
    title = get_input("Title: ")
    description = get_input("Description: ")
    date = get_date()
    
    post = {
        "author": author,
        "title": title,
        "description": description,
        "date": date
    }
    
    posts.append(post)
    print_message("Post created successfully!", "success")

def display_posts(posts_list):
    """Displays a list of posts in a clean format."""
    if not posts_list:
        print_message("No posts found.", "warning")
        return

    for post in posts_list:
        print("\n" + "-" * 50)
        print(f"Author: {post['author']}")
        print(f"Title:  {post['title']}")
        print(f"Date:   {post['date']}")
        print(f"Description:\n{post['description']}")
        print("-" * 50)

def view_all_posts():
    """Displays all posts."""
    print_header("Community Board - All Posts")
    display_posts(posts)

def search_posts_by_username():
    """Searches for posts created by a specific user."""
    print_header("Search Posts")
    username = get_input("Enter username to search for: ")
    
    filtered_posts = [p for p in posts if p['author'].lower() == username.lower()]
    
    print(f"\nShowing results for: {username}")
    display_posts(filtered_posts)
