import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author, genre, copies):
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = copies


class User:
    def __init__(self, name, user_type, interest):
        self.name = name
        self.user_type = user_type  
        self.interest = interest
        self.borrowed_books = []


books = [
    Book('Harry Potter', 'J.K.Rowling', 'Fantasy', 3),
    Book('Introduction to AI', 'Stuart Russell', 'Education', 2),
    Book('World History', 'John Doe', 'History', 1),
    Book('Data Science Handbook', 'Field Cady', 'Education', 1),
    Book('Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 2)
]

users = [
    User('Alice', 'Student', 'Fantasy'),
    User('Dr. Bob', 'Faculty', 'History'),
    User('Librarian', 'Librarian', 'All')
]


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Library Expert System")
        self.root.geometry("800x600")
        self.current_user = None
        
        self.create_login_screen()
    
    def create_login_screen(self):
        self.clear_window()
        
        tk.Label(self.root, text="===== Welcome to the Advanced Library Expert System =====", 
                font=('Helvetica', 14, 'bold')).pack(pady=20)
        
        tk.Label(self.root, text="Available Users:", font=('Helvetica', 12)).pack()
        
        self.user_listbox = tk.Listbox(self.root, height=10, width=50, font=('Helvetica', 12))
        self.user_listbox.pack(pady=10)
        
        for idx, user in enumerate(users, start=1):
            self.user_listbox.insert(tk.END, f"{idx}. {user.name} ({user.user_type})")
        
        tk.Button(self.root, text="Login", command=self.handle_login, 
                 font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(pady=10)
        
        tk.Button(self.root, text="Exit", command=self.root.quit,
                 font=('Helvetica', 12), bg='#f44336', fg='white').pack(pady=5)
    
    def handle_login(self):
        try:
            selection = self.user_listbox.curselection()[0]
            self.current_user = users[selection]
            
            if self.current_user.user_type.lower() == 'librarian':
                self.create_librarian_panel()
            else:
                self.create_user_panel()
        except IndexError:
            messagebox.showerror("Error", "Please select a user to login")
    
    def create_librarian_panel(self):
        self.clear_window()
        
        # Header
        tk.Label(self.root, text=f"📚 Librarian Panel: {self.current_user.name}", 
                font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        buttons = [
            ("View All Books", self.view_books),
            ("Add New Book", self.add_new_book_gui),
            ("Add New User", self.add_new_user_gui),
            ("Search Books", self.search_books_gui),
            ("Logout", self.create_login_screen)
        ]
        
        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command, 
                     width=20, font=('Helvetica', 12), bg='#2196F3', fg='white').pack(pady=5)
    
    def create_user_panel(self):
        self.clear_window()
        
        # Header
        tk.Label(self.root, text=f"Welcome, {self.current_user.name} ({self.current_user.user_type})!", 
                font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Info Frame
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text=f"Borrow Limit: {self.borrow_limit(self.current_user)} books", 
                font=('Helvetica', 12)).pack()
        
        # Buttons Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        buttons = [
            ("View Recommendations", self.view_recommendations_gui),
            ("View All Books", self.view_books),
            ("Search Books", self.search_books_gui),
            ("Borrow a Book", self.borrow_book_gui),
            ("Return a Book", self.return_book_gui),
            ("View Borrowed Books", self.view_borrowed_books_gui),
            ("Logout", self.create_login_screen)
        ]
        
        for text, command in buttons:
            tk.Button(button_frame, text=text, command=command, 
                     width=20, font=('Helvetica', 12), bg='#2196F3', fg='white').pack(pady=5)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def view_books(self):
        self.clear_window()
        
        tk.Label(self.root, text="📚 List of Books", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        # Treeview for books
        tree = ttk.Treeview(self.root, columns=('Title', 'Author', 'Genre', 'Copies', 'Status'), show='headings')
        tree.heading('Title', text='Title')
        tree.heading('Author', text='Author')
        tree.heading('Genre', text='Genre')
        tree.heading('Copies', text='Copies')
        tree.heading('Status', text='Status')
        
        for book in books:
            status = "Available" if book.copies > 0 else "Unavailable"
            tree.insert('', tk.END, values=(book.title, book.author, book.genre, book.copies, status))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def view_recommendations_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="📚 Recommended Books", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        recs = self.recommend_books(self.current_user)
        
        if recs:
            tree = ttk.Treeview(self.root, columns=('Title', 'Author', 'Genre', 'Copies'), show='headings')
            tree.heading('Title', text='Title')
            tree.heading('Author', text='Author')
            tree.heading('Genre', text='Genre')
            tree.heading('Copies', text='Copies')
            
            for book in recs:
                tree.insert('', tk.END, values=(book.title, book.author, book.genre, book.copies))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        else:
            tk.Label(self.root, text="No recommendations at the moment.", font=('Helvetica', 12)).pack(pady=20)
    
    def search_books_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="🔎 Search Books", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Search Frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search Keyword:", font=('Helvetica', 12)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=('Helvetica', 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.perform_search, 
                 font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(side=tk.LEFT)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        # Results Treeview
        self.search_tree = ttk.Treeview(self.root, columns=('Title', 'Author', 'Genre', 'Status'), show='headings')
        self.search_tree.heading('Title', text='Title')
        self.search_tree.heading('Author', text='Author')
        self.search_tree.heading('Genre', text='Genre')
        self.search_tree.heading('Status', text='Status')
        self.search_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def perform_search(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a search keyword")
            return
        
        results = self.search_books(keyword)
        self.search_tree.delete(*self.search_tree.get_children())
        
        if results:
            for book in results:
                status = "Available" if book.copies > 0 else "Unavailable"
                self.search_tree.insert('', tk.END, values=(book.title, book.author, book.genre, status))
        else:
            messagebox.showinfo("Info", "No matching books found")
    
    def borrow_book_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="📚 Borrow a Book", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        # Book Entry Frame
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)
        
        tk.Label(entry_frame, text="Book Title:", font=('Helvetica', 12)).pack(side=tk.LEFT)
        self.borrow_entry = tk.Entry(entry_frame, font=('Helvetica', 12), width=30)
        self.borrow_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(entry_frame, text="Borrow", command=self.perform_borrow, 
                 font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(side=tk.LEFT)
    
    def perform_borrow(self):
        book_title = self.borrow_entry.get().strip()
        if not book_title:
            messagebox.showwarning("Warning", "Please enter a book title")
            return
        
        self.borrow_book(self.current_user, book_title)
        self.borrow_entry.delete(0, tk.END)
    
    def return_book_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="📚 Return a Book", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        # Book Entry Frame
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)
        
        tk.Label(entry_frame, text="Book Title:", font=('Helvetica', 12)).pack(side=tk.LEFT)
        self.return_entry = tk.Entry(entry_frame, font=('Helvetica', 12), width=30)
        self.return_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(entry_frame, text="Return", command=self.perform_return, 
                 font=('Helvetica', 12), bg='#4CAF50', fg='white').pack(side=tk.LEFT)
    
    def perform_return(self):
        book_title = self.return_entry.get().strip()
        if not book_title:
            messagebox.showwarning("Warning", "Please enter a book title")
            return
        
        self.return_book(self.current_user, book_title)
        self.return_entry.delete(0, tk.END)
    
    def view_borrowed_books_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="📚 Borrowed Books", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        if not self.current_user.borrowed_books:
            tk.Label(self.root, text="No borrowed books.", font=('Helvetica', 12)).pack(pady=20)
        else:
            tree = ttk.Treeview(self.root, columns=('Title', 'Due Date'), show='headings')
            tree.heading('Title', text='Title')
            tree.heading('Due Date', text='Due Date')
            
            for book_title, due_date in self.current_user.borrowed_books:
                tree.insert('', tk.END, values=(book_title, due_date.strftime('%d-%m-%Y')))
            
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_new_user_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="➕ Add New User", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        # Form Frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Name:", font=('Helvetica', 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_user_name = tk.Entry(form_frame, font=('Helvetica', 12))
        self.new_user_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="User Type:", font=('Helvetica', 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_user_type = ttk.Combobox(form_frame, values=["Student", "Faculty"], font=('Helvetica', 12), state="readonly")
        self.new_user_type.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Interest:", font=('Helvetica', 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_user_interest = ttk.Combobox(form_frame, values=["Fantasy", "Education", "History", "All"], font=('Helvetica', 12))
        self.new_user_interest.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(form_frame, text="Add User", command=self.perform_add_user, 
                 font=('Helvetica', 12), bg='#4CAF50', fg='white').grid(row=3, columnspan=2, pady=10)
    
    def perform_add_user(self):
        name = self.new_user_name.get().strip()
        user_type = self.new_user_type.get().strip()
        interest = self.new_user_interest.get().strip()
        
        if not name or not user_type or not interest:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        users.append(User(name, user_type, interest))
        messagebox.showinfo("Success", f"User {name} added successfully")
        self.new_user_name.delete(0, tk.END)
        self.new_user_type.set('')
        self.new_user_interest.set('')
    
    def add_new_book_gui(self):
        self.clear_window()
        
        tk.Label(self.root, text="➕ Add New Book", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Back button
        tk.Button(self.root, text="Back", command=self.show_current_panel,
                 font=('Helvetica', 12), bg='#607D8B', fg='white').pack(pady=5)
        
        # Form Frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Title:", font=('Helvetica', 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_book_title = tk.Entry(form_frame, font=('Helvetica', 12))
        self.new_book_title.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Author:", font=('Helvetica', 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_book_author = tk.Entry(form_frame, font=('Helvetica', 12))
        self.new_book_author.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Genre:", font=('Helvetica', 12)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_book_genre = ttk.Combobox(form_frame, values=["Fantasy", "Education", "History", "Other"], font=('Helvetica', 12))
        self.new_book_genre.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Copies:", font=('Helvetica', 12)).grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.new_book_copies = tk.Entry(form_frame, font=('Helvetica', 12))
        self.new_book_copies.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Button(form_frame, text="Add Book", command=self.perform_add_book, 
                 font=('Helvetica', 12), bg='#4CAF50', fg='white').grid(row=4, columnspan=2, pady=10)
    
    def perform_add_book(self):
        title = self.new_book_title.get().strip()
        author = self.new_book_author.get().strip()
        genre = self.new_book_genre.get().strip()
        copies = self.new_book_copies.get().strip()
        
        if not title or not author or not genre or not copies:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        try:
            copies = int(copies)
            if copies < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Copies must be a positive integer")
            return
        
        books.append(Book(title, author, genre, copies))
        messagebox.showinfo("Success", f"Book '{title}' added successfully")
        self.new_book_title.delete(0, tk.END)
        self.new_book_author.delete(0, tk.END)
        self.new_book_genre.set('')
        self.new_book_copies.delete(0, tk.END)
    
    def show_current_panel(self):
        if self.current_user.user_type.lower() == 'librarian':
            self.create_librarian_panel()
        else:
            self.create_user_panel()
    
    # Original functions with slight modifications for GUI
    def check_availability(self, book):
        return 'Available' if book.copies > 0 else 'Unavailable'

    def recommend_books(self, user):
        return [book for book in books if book.genre.lower() == user.interest.lower() and book.copies > 0]

    def borrow_limit(self, user):
        if user.user_type.lower() == 'student':
            return 5
        elif user.user_type.lower() == 'faculty':
            return 10
        else:
            return 0  

    def borrow_book(self, user, book_title):
        for book in books:
            if book.title.lower() == book_title.lower():
                if book.copies > 0:
                    if len(user.borrowed_books) < self.borrow_limit(user):
                        book.copies -= 1
                        due_date = datetime.now() + timedelta(days=14)
                        user.borrowed_books.append((book.title, due_date))
                        messagebox.showinfo("Success", 
                            f"{book.title} issued to {user.name}. Due on {due_date.strftime('%d-%m-%Y')}.")
                    else:
                        messagebox.showwarning("Warning", "Borrow limit reached.")
                else:
                    messagebox.showwarning("Warning", "Book not available.")
                return
        messagebox.showwarning("Warning", "Book not found.")

    def return_book(self, user, book_title):
        for borrowed_book in user.borrowed_books:
            if borrowed_book[0].lower() == book_title.lower():
                for book in books:
                    if book.title.lower() == book_title.lower():
                        book.copies += 1
                user.borrowed_books.remove(borrowed_book)
                messagebox.showinfo("Success", f"{book_title} returned successfully.")
                return
        messagebox.showwarning("Warning", "You have not borrowed this book.")

    def search_books(self, keyword):
        results = []
        for book in books:
            if (keyword.lower() in book.title.lower() or 
                keyword.lower() in book.author.lower() or 
                keyword.lower() in book.genre.lower()):
                results.append(book)
        return results


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()