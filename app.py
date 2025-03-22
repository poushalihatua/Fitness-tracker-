import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Initialize Database
def init_db():
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        exercise TEXT NOT NULL,
                        duration INTEGER NOT NULL,
                        calories INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Function to Add Workout
def add_workout():
    date = date_entry.get()
    exercise = exercise_entry.get()
    duration = duration_entry.get()
    calories = calories_entry.get()

    if not date or not exercise or not duration or not calories:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workouts (date, exercise, duration, calories) VALUES (?, ?, ?, ?)",
                   (date, exercise, duration, calories))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Workout added successfully!")
    refresh_workouts()

# Function to Delete Workout
def delete_workout():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a workout to delete!")
        return
    
    workout_id = tree.item(selected_item, "values")[0]
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Deleted", "Workout deleted successfully!")
    refresh_workouts()

# Function to Display Workouts
def refresh_workouts():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts ORDER BY date DESC")
    workouts = cursor.fetchall()
    conn.close()
    
    for workout in workouts:
        tree.insert("", "end", values=workout)

# Create GUI Window
root = tk.Tk()
root.title("Personal Fitness Tracker")
root.geometry("500x400")

# Input Fields
tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Exercise:").pack()
exercise_entry = tk.Entry(root)
exercise_entry.pack()

tk.Label(root, text="Duration (minutes):").pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

tk.Label(root, text="Calories Burned:").pack()
calories_entry = tk.Entry(root)
calories_entry.pack()

# Buttons
tk.Button(root, text="Add Workout", command=add_workout).pack(pady=5)
tk.Button(root, text="Delete Selected Workout", command=delete_workout).pack(pady=5)

# Table to Display Workouts
columns = ("ID", "Date", "Exercise", "Duration", "Calories")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

# Initialize Database and Load Data
init_db()
refresh_workouts()

# Run GUI
root.mainloop()
