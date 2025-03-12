import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

# Sample juice menu with 20 juices and prices ranging from $20 to $150
menu = [
    {"name": "Orange Juice", "price": 20.0},
    {"name": "Apple Juice", "price": 25.0},
    {"name": "Mango Juice", "price": 30.0},
    {"name": "Carrot Juice", "price": 35.0},
    {"name": "Pineapple Juice", "price": 40.0},
    {"name": "Lemon Juice", "price": 45.0},
    {"name": "Grape Juice", "price": 50.0},
    {"name": "Watermelon Juice", "price": 55.0},
    {"name": "Papaya Juice", "price": 60.0},
    {"name": "Kiwi Juice", "price": 65.0},
    {"name": "Strawberry Juice", "price": 70.0},
    {"name": "Blueberry Juice", "price": 75.0},
    {"name": "Peach Juice", "price": 80.0},
    {"name": "Cherry Juice", "price": 85.0},
    {"name": "Guava Juice", "price": 90.0},
    {"name": "Passion Fruit Juice", "price": 95.0},
    {"name": "Coconut Juice", "price": 100.0},
    {"name": "Lime Juice", "price": 110.0},
    {"name": "Tomato Juice", "price": 120.0},
    {"name": "Avocado Juice", "price": 150.0},
]

# Global variables to store user details, order, and total price
user_name = None
user_email = None
order = []
total_price = 0.0
main_window = None
second_window = None
third_window = None
fourth_window = None

# Function to connect to the MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Your MySQL host (localhost for local server)
            user="root",       # Your MySQL username
            password="root",   # Your MySQL password
            database="moni1"   # The database you created
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
        return None

# Function to save user details to the database
def save_user_details(name, email):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        ''', (name, email))
        conn.commit()
        conn.close()

# Home Page: To input user details
def home_page():
    global main_window
    main_window = tk.Tk()
    main_window.title("Juice Shop")
    main_window.configure(bg="#D8B0D3")  # Lilac background color

    tk.Label(main_window, text="Welcome to the Juice Shop", font=("Arial", 20), bg="#D8B0D3").pack(pady=10)

    # User Details Entry
    tk.Label(main_window, text="Enter Your Name:", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
    name_entry = tk.Entry(main_window, width=30, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(main_window, text="Enter Your Email:", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
    email_entry = tk.Entry(main_window, width=30, font=("Arial", 12))
    email_entry.pack(pady=5)

    # Next Page Button
    def next_page():
        global user_name, user_email
        user_name = name_entry.get()
        user_email = email_entry.get()

        if not user_name or not user_email:
            messagebox.showerror("Input Error", "Both name and email must be provided.")
            return
       
        # Save user details to the database
        save_user_details(user_name, user_email)

        # Close the current window and go to the next page
        main_window.destroy()  # Destroy the home window
        menu_page()  # Go to the second page
   
    tk.Button(main_window, text="Next", command=next_page, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=10)

    main_window.mainloop()

# Menu Page: To display juices and allow selection
def menu_page():
    global second_window, order, total_price
    second_window = tk.Tk()  # Create a new window
    second_window.title("Select Your Juices")
    second_window.configure(bg="#D8B0D3")  # Lilac background color

    tk.Label(second_window, text="Juice Menu", font=("Arial", 16), bg="#D8B0D3").pack(pady=10)

    # Create a listbox to display juice options
    juice_listbox = tk.Listbox(second_window, selectmode=tk.MULTIPLE, height=10, width=50, font=("Arial", 12))
    juice_listbox.pack(pady=10)

    # Add available juices to the listbox
    for juice in menu:
        juice_listbox.insert(tk.END, f"{juice['name']} - ${juice['price']}")

    # Function to handle adding juices to the order
    def add_to_order():
        global order, total_price
        selected_items = juice_listbox.curselection()
       
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select at least one juice.")
            return
       
        order = []
        total_price = 0.0
       
        for item in selected_items:
            juice = menu[item]
            order.append(juice)
            total_price += juice['price']

        confirmation_page()  # Show confirmation within the same window

    tk.Button(second_window, text="Add to Order", command=add_to_order, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

    second_window.mainloop()

# Confirmation Page: To confirm order details
def confirmation_page():
    global third_window
    third_window = tk.Tk()
    third_window.title("Confirm Your Order")
    third_window.configure(bg="#D8B0D3")  # Lilac background color

    tk.Label(third_window, text="Order Confirmation", font=("Arial", 16), bg="#D8B0D3").pack(pady=10)

    # Show selected juices and total price
    if order:
        tk.Label(third_window, text="Your Order:", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
        for juice in order:
            tk.Label(third_window, text=f"{juice['name']} - ${juice['price']}", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
       
        tk.Label(third_window, text=f"Total Price: ${total_price}", bg="#D8B0D3", font=("Arial", 14)).pack(pady=10)
   
    # Display user details
    tk.Label(third_window, text=f"Name: {user_name}", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
    tk.Label(third_window, text=f"Email: {user_email}", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)

    # Confirm Booking Button
    def confirm_order():
        thank_you_page()  # Go to Thank You page after confirmation

    tk.Button(third_window, text="Confirm Order", command=confirm_order, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

    # Go back to the menu page to modify the order
    def back_to_menu():
        # Clear confirmation labels and go back to order selection
        for widget in third_window.winfo_children():
            widget.destroy()
        menu_page()

    tk.Button(third_window, text="Modify Order", command=back_to_menu, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=5)

# Thank You Page: To display a Thank You message
def thank_you_page():
    global fourth_window
    fourth_window = tk.Tk()
    fourth_window.title("Thank You!")
    fourth_window.configure(bg="#D8B0D3")  # Lilac background color

    tk.Label(fourth_window, text="Thank You for Your Order!", font=("Arial", 20), bg="#D8B0D3").pack(pady=10)

    # Display order details
    tk.Label(fourth_window, text=f"Name: {user_name}", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
    tk.Label(fourth_window, text=f"Email: {user_email}", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
    for juice in order:
        tk.Label(fourth_window, text=f"{juice['name']} - ${juice['price']}", bg="#D8B0D3", font=("Arial", 12)).pack(pady=5)
   
    tk.Label(fourth_window, text=f"Total Price: ${total_price}", bg="#D8B0D3", font=("Arial", 14)).pack(pady=10)

    # Feedback Page Button
    def feedback_page():
        feedback_window = tk.Tk()
        feedback_window.title("Feedback")
        feedback_window.configure(bg="#D8B0D3")

        tk.Label(feedback_window, text="We Value Your Feedback", font=("Arial", 20), bg="#D8B0D3").pack(pady=10)

        feedback_entry = tk.Entry(feedback_window, width=50, font=("Arial", 12))
        feedback_entry.pack(pady=10)

        def submit_feedback():
            feedback = feedback_entry.get()
            if feedback:
                messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
                feedback_window.quit()
            else:
                messagebox.showerror("Error", "Please provide feedback before submitting.")

        tk.Button(feedback_window, text="Submit Feedback", command=submit_feedback, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

        feedback_window.mainloop()

    tk.Button(fourth_window, text="Give Feedback", command=feedback_page, bg="#FF8C00", fg="white", font=("Arial", 14)).pack(pady=20)

    fourth_window.mainloop()

# Start the app by calling the home page
home_page()



-----------------------------------------------


CREATE TABLE IF NOT EXISTS users (
       id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         email VARCHAR(255) NOT NULL,
         phone VARCHAR(15) NOT NULL
     );

-----------------------------------