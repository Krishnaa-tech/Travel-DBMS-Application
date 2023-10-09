import os
import sqlite3
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, PhotoImage
from datetime import datetime
from tkcalendar import Calendar

# Create a SQLite database and a table for destinations
def create_database():
    conn = sqlite3.connect('travel_planner.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS destinations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT, destination TEXT, date DATE, time_taken TEXT, expenses FLOAT, days INTEGER, num_people INTEGER, status TEXT)''')
    conn.commit()
    conn.close()

# Create a class for the Travel Planner App
class TravelPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Travel Planner")
        self.geometry('1920x1200')
        self.configure(bg="light gray")
        self.iconbitmap('travel_logo.ico')
        # self.date_calendar = Calendar(self, selectmode="day", date_pattern="dd/mm/yyyy", font=("Arial", 15))
        # self.date_calendar.pack()
        # self.date_calendar_button = tk.Button(self, text="Select Date", command=self.get_selected_date, font=("Arial", 15))
        # self.date_calendar_button.pack()


        # Load the logo image
        logo_image = PhotoImage(file='travel_logo.png')
        tk.Label(self, image=logo_image, bg='#F99D27').pack()

        # Load the background image
        self.background_image = Image.open("background_img.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        background_label = tk.Label(self, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window

       # Create an entry field for the number of people
        self.people_label = tk.Label(self, text="Number of People:", font=("Arial", 15, "bold"))
        self.people_entry = tk.Entry(self, font=("Arial", 15))

        # _____________________________Heading of the App___________________________

        label = tk.Label(self, text="WELCOME TO THE TRAVEL TECH", font=("Times New Roman", 26))
        label.pack()

        # Initialize database
        create_database()

        # Create fonts
        custom_font = tk.font.Font(size=15, weight='bold')

        # Create widgets with improved styling
        self.source_label = tk.Label(self, text="Source:", font=("Arial", 15, "bold"))
        self.source_entry = tk.Entry(self, font=("Arial", 15))
        self.destination_label = tk.Label(self, text="Destination:", font=("Arial", 15, "bold"))
        self.destination_entry = tk.Entry(self, font=("Arial", 15))
        self.date_label = tk.Label(self, text="Date:", font=("Arial", 15, "bold"))
        self.date_entry = tk.Entry(self, font=("Arial", 15))
        self.time_taken_label = tk.Label(self, text="Time Taken(Hrs):", font=("Arial", 15, "bold"))
        self.time_taken_entry = tk.Entry(self, font=("Arial", 15))
        self.expenses_label = tk.Label(self, text="Expenses(\u20B9):", font=("Arial", 15, "bold"))
        self.expenses_entry = tk.Entry(self, font=("Arial", 15))
        self.days_label = tk.Label(self, text="Number of Days of Stay:", font=("Arial", 15, "bold"))
        self.days_entry = tk.Entry(self, font=("Arial", 15))
        self.date_format_label = tk.Label(self, text="Date Format:", font=("Arial", 15, "bold"))
        self.date_format_var = tk.StringVar()
        self.date_format_combo = ttk.Combobox(self, textvariable=self.date_format_var, values=["DD/MM/YYYY", "MM/DD/YYYY"], font=("Arial", 15))
        self.date_format_combo.set("DD/MM/YYYY")
        self.add_button = tk.Button(self, text="Add Destination", command=self.add_destination, bg="green", fg="white", font=("Arial", 15, "bold"))
        self.remove_button = tk.Button(self, text="Remove Destination", command=self.remove_destination, bg="red", fg="white", font=("Arial", 15, "bold"))
        self.destination_listbox = tk.Listbox(self, font=("Arial", 15))
        self.visited_listbox = tk.Listbox(self, font=("Arial", 15))
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.destination_listbox.config(yscrollcommand=self.scrollbar.set)
        self.visited_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.destination_listbox.yview)
        self.scrollbar.config(command=self.visited_listbox.yview)
        self.status_label = tk.Label(self, text="", fg="black", font=("Arial", 15))


        # Pack widgets
        self.source_label.pack()
        self.source_entry.pack()
        self.destination_label.pack()
        self.destination_entry.pack()
        self.date_label.pack()
        self.date_entry.pack()
        self.time_taken_label.pack()
        self.time_taken_entry.pack()
        self.expenses_label.pack()
        self.expenses_entry.pack()
        self.days_label.pack()
        self.days_entry.pack()
        self.people_label.pack()
        self.people_entry.pack()
        self.date_format_label.pack()
        self.date_format_combo.pack()
        self.add_button.pack()
        self.remove_button.pack()
        self.destination_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.visited_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_label.pack()

        # Create buttons to move destinations
        self.move_to_visited_button = tk.Button(self, text="Move to Visited", command=self.move_to_visited, bg="blue", fg="white", font=("Arial", 15, "bold"))
        self.move_to_visited_button.pack()

        self.move_to_to_visit_button = tk.Button(self, text="Move to To Visit", command=self.move_to_to_visit, bg="orange", fg="white", font=("Arial", 15, "bold"))
        self.move_to_to_visit_button.pack()

        # Add a button to view destinations
        self.view_button = tk.Button(self, text="View Destinations", command=self.view_destinations, bg="purple", fg="white", font=("Arial", 15, "bold"))
        self.view_button.pack()

        # Create a Treeview widget for displaying destinations
        self.destination_table = ttk.Treeview(self, columns=("ID", "Source", "Destination", "Date", "Time Taken", "Expenses", "Days","Num of People" ,"Status"), show="headings")
        self.destination_table.heading("ID", text="ID")
        self.destination_table.heading("Source", text="Source")
        self.destination_table.heading("Destination", text="Destination")
        self.destination_table.heading("Date", text="Date")
        self.destination_table.heading("Time Taken", text="Time Taken")
        self.destination_table.heading("Expenses", text="Expenses")
        self.destination_table.heading("Days", text="Days")
        self.destination_table.heading("Num of People", text="Num of People")
        self.destination_table.heading("Status", text="Status")
        self.destination_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Initialize destination lists
        self.refresh_lists()

        # Close the database connection when the app is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_destination(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()
        date = self.date_entry.get()
        time_taken = self.time_taken_entry.get()
        expenses = self.expenses_entry.get()
        days = self.days_entry.get()
        num_people = self.people_entry.get()
        status = "To Visit"

        # Validate input fields
        if not all([source, destination, date, time_taken, expenses, num_people, days]):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        # Parse date if necessary
        if self.date_format_var.get() == "DD/MM/YYYY":
            try:
                date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format! Use DD/MM/YYYY.")
                return

        # Insert destination into database
        conn = sqlite3.connect('travel_planner.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO destinations (source, destination, date, time_taken, expenses, days, num_people, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (source, destination, date, time_taken, expenses, days, num_people, status))
        conn.commit()
        conn.commit()
        conn.close()

        # Update UI and status label
        self.to_visit_destinations.append(f"{source} to {destination} ({date})")
        self.refresh_lists()
        self.status_label.config(text="Destination added successfully!", fg="green")

    def remove_destination(self):
        selected_index = self.destination_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            destination = self.to_visit_destinations.pop(index)
            conn = sqlite3.connect('travel_planner.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM destinations WHERE destination=?", (destination.split("(")[0].strip(),))
            conn.commit()
            conn.close()
            self.refresh_lists()
            self.status_label.config(text="Destination removed successfully!", fg="green")
        else:
            messagebox.showwarning("Warning", "Select a destination to remove!")
            self.status_label.config(text="Select a destination to remove!", fg="red")

    def move_to_visited(self):
        selected_index = self.destination_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            destination = self.to_visit_destinations.pop(index)
            self.visited_destinations.append(destination)

            # Update the destination's status in the destination list
            destination_index = None
            for i, dest in enumerate(self.visited_destinations):
                if destination in dest:
                    destination_index = i
                    break

            if destination_index is not None:
                self.visited_destinations[destination_index] = destination.replace("To Visit", "Visited")

            # Update the database status
            conn = sqlite3.connect('travel_planner.db')
            cursor = conn.cursor()
            query = "UPDATE destinations SET status=? WHERE destination=?"
            try:
                cursor.execute(query, ("Visited", destination.split("(")[0].strip()))
                conn.commit()
                conn.close()
                self.refresh_lists()
                self.status_label.config(text="Destination moved to 'Visited'!", fg="green")
            except sqlite3.Error as e:
                conn.rollback()
                print("SQLite error:", e)
                self.status_label.config(text="Error updating status!", fg="red")
        else:
            messagebox.showwarning("Warning", "Select a destination to move to 'Visited'!")
            self.status_label.config(text="Select a destination to move to 'Visited'!", fg="red")

    def move_to_to_visit(self):
        selected_index = self.visited_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            destination = self.visited_destinations.pop(index)
            self.to_visit_destinations.append(destination)

            # Update the destination's status in the destination list
            destination_index = None
            for i, dest in enumerate(self.to_visit_destinations):
                if destination in dest:
                    destination_index = i
                    break

            if destination_index is not None:
                self.to_visit_destinations[destination_index] = destination.replace("Visited", "To Visit")

            # Update the database status
            conn = sqlite3.connect('travel_planner.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE destinations SET status=? WHERE destination=?", ("To Visit", destination.split("(")[0].strip()))
            conn.commit()
            conn.close()

            self.refresh_lists()
            self.status_label.config(text="Destination moved to 'To Visit'!", fg="green")
        else:
            messagebox.showwarning("Warning", "Select a destination to move to 'To Visit'!")
            self.status_label.config(text="Select a destination to move to 'To Visit'!", fg="red")

    def view_destinations(self):
        view_window = tk.Toplevel(self)
        view_window.title("View Destinations")

        # Create a Treeview widget for the table
        columns = ("ID", "Source", "Destination", "Date", "Time Taken", "Expenses", "Days", "Num People" ,"Status")
        destination_table = ttk.Treeview(view_window, columns=columns, show="headings")

        # Set column headings
        for col in columns:
            destination_table.heading(col, text=col)
            destination_table.column(col, width=100) 

        # Retrieve data from the database and populate the table
        conn = sqlite3.connect('travel_planner.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destinations")
        data = cursor.fetchall()
        for row in data:
            destination_table.insert("", "end", values=row)

        destination_table.pack()

    def refresh_lists(self):
        self.destination_listbox.delete(0, tk.END)
        self.visited_listbox.delete(0, tk.END)

        self.to_visit_destinations = []
        self.visited_destinations = []

        conn = sqlite3.connect('travel_planner.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM destinations")
        data = cursor.fetchall()
        for row in data:
            destination = f"{row[1]} to {row[2]} ({row[3]})"
            if row[7] == "To Visit":
                self.to_visit_destinations.append(destination)
            elif row[7] == "Visited":
                self.visited_destinations.append(destination)

        for destination in self.to_visit_destinations:
            self.destination_listbox.insert(tk.END, destination)

        for destination in self.visited_destinations:
            self.visited_listbox.insert(tk.END, destination)

    def on_closing(self):
        self.destroy()

    # method to get the selected date
    def get_selected_date(self):
        selected_date = self.date_calendar.get_date()
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, selected_date)

if __name__ == "__main__":
    app = TravelPlannerApp()
    app.mainloop()









