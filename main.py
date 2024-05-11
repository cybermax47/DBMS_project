# import psycopg2
# from configparser import ConfigParser

# def config(filename='database.ini', section='postgresql'):
#     parser = ConfigParser()
#     parser.read(filename)
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception(f'Section {section} not found in the {filename} file')
#     return db

# def get_db_connection():
#     try:
#         params = config()
#         return psycopg2.connect(**params)
#     except psycopg2.Error as e:
#         print(f"Unable to connect to the database: {e}")
#         return None

# def add_user():
#     connection = get_db_connection()
#     if connection is None:
#         return
#     try:
#         cursor = connection.cursor()
#         id = int(input("Enter user ID: "))
#         email = input("Enter user email: ")
#         password = input("Enter user password: ")
#         remember_token = input("Enter remember token (True/False): ")
#         cursor.execute("INSERT INTO users (id, email, password, remember_token) VALUES (%s, %s, %s, %s)",
#                        (id, email, password, remember_token))
#         connection.commit()
#         print("User added successfully.")
#     except (psycopg2.Error, ValueError) as error:
#         print(f"Error while adding user: {error}")
#     finally:
#         connection.close()

# def add_contact():
#     connection = get_db_connection()
#     if connection is None:
#         return
#     try:
#         cursor = connection.cursor()
#         name = input("Enter your name: ")
#         email = input("Enter your email: ")
#         subject = input("Enter subject: ")
#         message = input("Enter message: ")
#         cursor.execute("INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)",
#                        (name, email, subject, message))
#         connection.commit()
#         print("Contact information added successfully.")
#     except (psycopg2.Error, ValueError) as error:
#         print(f"Error while adding contact: {error}")
#     finally:
#         connection.close()

# def add_booking():
#     connection = get_db_connection()
#     try:
#         cursor = connection.cursor()
#         user_id = int(input("Enter User ID: "))
#         package_id = int(input("Enter Package ID: "))
#         num_guests = int(input("Enter Number of Guests: "))
#         arrival_date = input("Enter Arrival Date (YYYY-MM-DD): ")

#         cursor.execute("INSERT INTO bookings (user_id, package_id, num_guests, arrival_date) VALUES (%s, %s, %s, %s)",
#                        (user_id, package_id, num_guests, arrival_date))
#         connection.commit()
#         print("Booking added successfully.")
#     except (psycopg2.Error, ValueError) as error:
#         print("Error while adding booking:", error)
#     finally:
#         if connection:
#             connection.close()


# # Function to add a new package
# def add_package():
#     try:
#         connection = get_db_connection()
#         cursor = connection.cursor()
        
#         name = input("Enter package name: ")
#         description = input("Enter package description: ")
#         location = input("Enter package location: ")
#         price_current = float(input("Enter current price: "))
#         price_old = float(input("Enter old price: "))
#         stars = int(input("Enter number of stars (0-5): "))

#         cursor.execute("INSERT INTO packages (name, description, location, price_current, price_old, stars) VALUES (%s, %s, %s, %s, %s, %s)",
#                        (name, description, location, price_current, price_old, stars))
#         connection.commit()
#         print("Package added successfully.")
#     except (psycopg2.Error, ValueError) as error:
#         print("Error while adding package:", error)
#     finally:
#         if connection:
#             connection.close()


# def main_menu():
#     options = {
#         '1': add_user,
#         '2': add_package,
#         '3': add_booking,
#         '4': add_contact,
#         '5': lambda: print("Exiting...")
#     }
#     while True:
#         print("\nTOUR MANAGEMENT SYSTEM")
#         print("1. Add User")
#         print("2. Add Package")
#         print("3. Add Booking")
#         print("4. Add Contact")
#         print("5. Exit")
#         choice = input("Enter your choice: ")
#         action = options.get(choice)
#         if action:
#             action()
#         else:
#             print("Invalid choice. Please try again.")

# if __name__ == "__main__":
#     main_menu()




######################################################################################################################

import tkinter as tk
from tkinter import Toplevel, messagebox, Entry, Label, Button
import psycopg2
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db

def get_db_connection():
    try:
        params = config()
        return psycopg2.connect(**params)
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", f"Unable to connect to the database: {e}")
        return None

def add_user(window):
    try:
        connection = get_db_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        id = int(window.entry_user_id.get())
        email = window.entry_email.get()
        password = window.entry_password.get()
        remember_token = window.entry_remember_token.get()
        cursor.execute("INSERT INTO users (id, email, password, remember_token) VALUES (%s, %s, %s, %s)",
                       (id, email, password, remember_token))
        connection.commit()
        messagebox.showinfo("Success", "User added successfully.")
    except (psycopg2.Error, ValueError) as error:
        messagebox.showerror("Error", f"Error while adding user: {error}")
    finally:
        if connection:
            connection.close()
        window.destroy()

def add_contact(window):
    try:
        connection = get_db_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        name = window.entry_name.get()
        email = window.entry_contact_email.get()
        subject = window.entry_subject.get()
        message = window.entry_message.get()
        cursor.execute("INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                       (name, email, subject, message))
        connection.commit()
        messagebox.showinfo("Success", "Contact information added successfully.")
    except (psycopg2.Error, ValueError) as error:
        messagebox.showerror("Error", f"Error while adding contact: {error}")
    finally:
        if connection:
            connection.close()
        window.destroy()

def add_booking(window):
    try:
        connection = get_db_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        user_id = int(window.entry_booking_user_id.get())
        package_id = int(window.entry_package_id.get())
        num_guests = int(window.entry_num_guests.get())
        arrival_date = window.entry_arrival_date.get()
        cursor.execute("INSERT INTO bookings (user_id, package_id, num_guests, arrival_date) VALUES (%s, %s, %s, %s)",
                       (user_id, package_id, num_guests, arrival_date))
        connection.commit()
        messagebox.showinfo("Success", "Booking added successfully.")
    except (psycopg2.Error, ValueError) as error:
        messagebox.showerror("Error", f"Error while adding booking: {error}")
    finally:
        if connection:
            connection.close()
        window.destroy()

def add_package(window):
    try:
        connection = get_db_connection()
        if connection is None:
            return
        cursor = connection.cursor()
        name = window.entry_package_name.get()
        description = window.entry_description.get()
        location = window.entry_location.get()
        price_current = float(window.entry_price_current.get())
        price_old = float(window.entry_price_old.get())
        stars = int(window.entry_stars.get())
        cursor.execute("INSERT INTO packages (name, description, location, price_current, price_old, stars) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, description, location, price_current, price_old, stars))
        connection.commit()
        messagebox.showinfo("Success", "Package added successfully.")
    except (psycopg2.Error, ValueError) as error:
        messagebox.showerror("Error", f"Error while adding package: {error}")
    finally:
        if connection:
            connection.close()
        window.destroy()

def open_form(window_class):
    window = window_class()
    window.grab_set()

class UserWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Add User")
        Label(self, text="User ID:").pack()
        self.entry_user_id = Entry(self)
        self.entry_user_id.pack()

        Label(self, text="Email:").pack()
        self.entry_email = Entry(self)
        self.entry_email.pack()

        Label(self, text="Password:").pack()
        self.entry_password = Entry(self)
        self.entry_password.pack()

        Label(self, text="Remember Token (True/False):").pack()
        self.entry_remember_token = Entry(self)
        self.entry_remember_token.pack()

        Button(self, text="Submit", command=lambda: add_user(self)).pack()

class ContactWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Add Contact")
        Label(self, text="Name:").pack()
        self.entry_name = Entry(self)
        self.entry_name.pack()

        Label(self, text="Email:").pack()
        self.entry_contact_email = Entry(self)
        self.entry_contact_email.pack()

        Label(self, text="Subject:").pack()
        self.entry_subject = Entry(self)
        self.entry_subject.pack()

        Label(self, text="Message:").pack()
        self.entry_message = Entry(self)
        self.entry_message.pack()

        Button(self, text="Submit", command=lambda: add_contact(self)).pack()

class BookingWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Add Booking")
        Label(self, text="User ID:").pack()
        self.entry_booking_user_id = Entry(self)
        self.entry_booking_user_id.pack()

        Label(self, text="Package ID:").pack()
        self.entry_package_id = Entry(self)
        self.entry_package_id.pack()

        Label(self, text="Number of Guests:").pack()
        self.entry_num_guests = Entry(self)
        self.entry_num_guests.pack()

        Label(self, text="Arrival Date (YYYY-MM-DD):").pack()
        self.entry_arrival_date = Entry(self)
        self.entry_arrival_date.pack()

        Button(self, text="Submit", command=lambda: add_booking(self)).pack()

class PackageWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Add Package")
        Label(self, text="Package Name:").pack()
        self.entry_package_name = Entry(self)
        self.entry_package_name.pack()

        Label(self, text="Description:").pack()
        self.entry_description = Entry(self)
        self.entry_description.pack()

        Label(self, text="Location:").pack()
        self.entry_location = Entry(self)
        self.entry_location.pack()

        Label(self, text="Current Price:").pack()
        self.entry_price_current = Entry(self)
        self.entry_price_current.pack()

        Label(self, text="Old Price:").pack()
        self.entry_price_old = Entry(self)
        self.entry_price_old.pack()

        Label(self, text="Stars (0-5):").pack()
        self.entry_stars = Entry(self)
        self.entry_stars.pack()

        Button(self, text="Submit", command=lambda: add_package(self)).pack()

def user_interface():
    user_window = Toplevel()
    user_window.title("User Interface")

    def new_user():
        new_user_window = Toplevel()
        new_user_window.title("New User")
        Label(new_user_window, text="Enter user details:").pack()

        user_id_label = Label(new_user_window, text="User ID:")
        user_id_label.pack()
        user_id_entry = Entry(new_user_window)
        user_id_entry.pack()

        email_label = Label(new_user_window, text="Email:")
        email_label.pack()
        email_entry = Entry(new_user_window)
        email_entry.pack()

        password_label = Label(new_user_window, text="Password:")
        password_label.pack()
        password_entry = Entry(new_user_window)
        password_entry.pack()

        remember_token_label = Label(new_user_window, text="Remember Token (True/False):")
        remember_token_label.pack()
        remember_token_entry = Entry(new_user_window)
        remember_token_entry.pack()

        def add_user_to_db():
            try:
                connection = get_db_connection()
                if connection is None:
                    return
                cursor = connection.cursor()
                id = int(user_id_entry.get())
                email = email_entry.get()
                password = password_entry.get()
                remember_token = remember_token_entry.get()
                cursor.execute("INSERT INTO users (id, email, password, remember_token) VALUES (%s, %s, %s, %s)",
                               (id, email, password, remember_token))
                connection.commit()
                messagebox.showinfo("Success", "User added successfully.")
            except (psycopg2.Error, ValueError) as error:
                messagebox.showerror("Error", f"Error while adding user: {error}")
            finally:
                if connection:
                    connection.close()
                new_user_window.destroy()

        Button(new_user_window, text="Submit", command=add_user_to_db).pack()

    def existing_user():
        def verify_user(user_id):
            try:
                connection = get_db_connection()
                if connection is None:
                    return False
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                if user:
                    return True
                else:
                    messagebox.showinfo("User Not Found", "User ID not found in the database.")
                    return False
            except psycopg2.Error as error:
                messagebox.showerror("Database Error", f"Error while verifying user: {error}")
                return False
            finally:
                if connection:
                    connection.close()

        def display_packages():
            messagebox.showinfo("Functionality", "Displaying packages")

        def add_booking():
            messagebox.showinfo("Functionality", "Adding booking")

        def add_contact():
            messagebox.showinfo("Functionality", "Adding contact")

        existing_user_window = Toplevel()
        existing_user_window.title("Existing User")
        Label(existing_user_window, text="Enter user ID:").pack()
        user_id_entry = Entry(existing_user_window)
        user_id_entry.pack()

        def on_submit():
            user_id = int(user_id_entry.get())
            if verify_user(user_id):
                user_options_window = Toplevel(existing_user_window)
                user_options_window.title("User Options")
                Button(user_options_window, text="Display Packages", command=display_packages).pack()
                Button(user_options_window, text="Add Booking", command=add_booking).pack()
                Button(user_options_window, text="Add Contact", command=add_contact).pack()

        Button(existing_user_window, text="Submit", command=on_submit).pack()

    Button(user_window, text="New User", command=new_user).pack()
    Button(user_window, text="Existing User", command=existing_user).pack()

def admin_interface():
    window = Toplevel()
    window.title("Admin Interface")
    Button(window, text="Add Package", command=lambda: open_form(PackageWindow)).pack(fill=tk.X)
    Button(window, text="Display Bookings", command=lambda: open_form(BookingWindow)).pack(fill=tk.X)
    Button(window, text="Display Contacts", command=lambda: open_form(ContactWindow)).pack(fill=tk.X)

# Main Application Window and Event Loop
root = tk.Tk()
root.title("Tour Management System")
Button(root, text="User", command=user_interface).pack(fill=tk.X)
Button(root, text="Admin", command=admin_interface).pack(fill=tk.X)
root.mainloop()
