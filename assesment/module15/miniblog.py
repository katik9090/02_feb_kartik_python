import tkinter as tk
from tkinter import messagebox, ttk
import os

class User:
    """Class to represent a Blog User."""
    def __init__(self, username):
        self.username = username

class Post:
    """Class to represent a Blog Post."""
    def __init__(self, user, title, content):
        self.user = user
        self.title = title
        self.content = content

    def get_filename(self):
        # Using a sanitized filename approach to avoid issues with special characters
        safe_user = "".join(x for x in self.user.username if x.isalnum() or x in "._- ")
        safe_title = "".join(x for x in self.title if x.isalnum() or x in "._- ")
        return f"{safe_user}_{safe_title}.txt"

class MiniBlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniBlog - Desktop Post Manager")
        self.root.geometry("700x600")
        self.root.configure(bg="#f4f7f6")

        # Custom Fonts
        self.title_font = ("Helvetica", 18, "bold")
        self.label_font = ("Helvetica", 10, "bold")
        self.entry_font = ("Helvetica", 10)

        self.setup_ui()
        self.refresh_post_list()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", pady=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="MiniBlog Assessment", font=self.title_font, fg="white", bg="#2c3e50").pack()

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f4f7f6", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left Panel: Creation
        creation_frame = tk.LabelFrame(main_frame, text=" Create New Post ", font=self.label_font, bg="#f4f7f6", padx=10, pady=10)
        creation_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(creation_frame, text="Username:", font=self.label_font, bg="#f4f7f6").grid(row=0, column=0, sticky="w", pady=(5, 0))
        self.username_entry = tk.Entry(creation_frame, font=self.entry_font, width=30)
        self.username_entry.grid(row=1, column=0, pady=(0, 10))

        tk.Label(creation_frame, text="Post Title:", font=self.label_font, bg="#f4f7f6").grid(row=2, column=0, sticky="w", pady=(5, 0))
        self.title_entry = tk.Entry(creation_frame, font=self.entry_font, width=30)
        self.title_entry.grid(row=3, column=0, pady=(0, 10))

        tk.Label(creation_frame, text="Content:", font=self.label_font, bg="#f4f7f6").grid(row=4, column=0, sticky="w", pady=(5, 0))
        self.content_text = tk.Text(creation_frame, font=self.entry_font, width=30, height=10)
        self.content_text.grid(row=5, column=0, pady=(0, 10))

        self.save_btn = tk.Button(creation_frame, text="Save Post", command=self.save_post, 
                                  bg="#27ae60", fg="white", font=self.label_font, padx=20, pady=5, relief=tk.FLAT)
        self.save_btn.grid(row=6, column=0, pady=10)

        # Right Panel: Viewing
        view_frame = tk.LabelFrame(main_frame, text=" Saved Posts ", font=self.label_font, bg="#f4f7f6", padx=10, pady=10)
        view_frame.grid(row=0, column=1, sticky="nsew")

        tk.Label(view_frame, text="Select a Post to View:", font=self.label_font, bg="#f4f7f6").pack(anchor="w")
        
        list_container = tk.Frame(view_frame)
        list_container.pack(fill=tk.BOTH, expand=True, pady=5)

        self.post_listbox = tk.Listbox(list_container, font=self.entry_font, width=40)
        self.post_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.post_listbox.bind('<<ListboxSelect>>', self.view_post)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.post_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.post_listbox.yview)

        self.refresh_btn = tk.Button(view_frame, text="Refresh List", command=self.refresh_post_list,
                                     bg="#2980b9", fg="white", font=self.label_font, padx=10, pady=2, relief=tk.FLAT)
        self.refresh_btn.pack(pady=5)

        tk.Label(view_frame, text="Post Content Preview:", font=self.label_font, bg="#f4f7f6").pack(anchor="w", pady=(10, 0))
        self.preview_text = tk.Text(view_frame, font=self.entry_font, width=40, height=8, state=tk.DISABLED, bg="#ecf0f1")
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Configure weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    def save_post(self):
        username = self.username_entry.get().strip()
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not username or not title or not content:
            messagebox.showwarning("Empty Fields", "All fields (Username, Title, Content) are required!")
            return

        try:
            user_obj = User(username)
            post_obj = Post(user_obj, title, content)
            filename = post_obj.get_filename()

            with open(filename, "w") as f:
                f.write(f"Author: {username}\nTitle: {title}\n\n{content}")

            messagebox.showinfo("Success", f"Post saved successfully as {filename}")
            
            # Clear fields
            self.username_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)
            
            self.refresh_post_list()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save post: {str(e)}")

    def refresh_post_list(self):
        self.post_listbox.delete(0, tk.END)
        # Scan current directory for .txt files
        files = [f for f in os.listdir(".") if f.endswith(".txt")]
        for f in files:
            self.post_listbox.insert(tk.END, f)

    def view_post(self, event):
        selection = self.post_listbox.curselection()
        if not selection:
            return
        
        filename = self.post_listbox.get(selection[0])
        
        try:
            with open(filename, "r") as f:
                content = f.read()
            
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert(tk.END, content)
            self.preview_text.config(state=tk.DISABLED)

        except FileNotFoundError:
            messagebox.showerror("Error", "Selected file not found.")
            self.refresh_post_list()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniBlogApp(root)
    root.mainloop()
