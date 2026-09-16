import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")
conn.commit()

# step2: Create a functions
# CREATE
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return
    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()
    messagebox.showinfo(
        "Success",
        "Student added successfully."
    )
    clear_fields()
    display_students()

# READ
def display_students():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    for student in students:
        tree.insert("", tk.END, values=student)

# UPDATE
def update_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to update."
        )
        return
    student_id = tree.item(selected[0])["values"][0]
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    if name == "" or age == "" or course == "":
        messagebox.showwarning(
            "Warning",
            "Please fill in all fields."
        )
        return
    try:
        age = int(age)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number."
        )
        return
    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?
        WHERE id = ?
    """, (name, age, course, student_id))
    conn.commit()
    messagebox.showinfo(
        "Success",
        "Student updated successfully."
    )
    clear_fields()
    display_students()

# DELETE
def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a student to delete."
        )
        return
    student_id = tree.item(selected[0])["values"][0]
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )
    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        conn.commit()
        messagebox.showinfo(
            "Success",
            "Student deleted successfully."
        )
        clear_fields()
        display_students()

# CLEAR INPUTS
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

# SELECT STUDENT
def select_student(event):
    selected = tree.selection()
    if selected:
        student = tree.item(selected[0])["values"]
        clear_fields()
        name_entry.insert(0, student[1])
        age_entry.insert(0, student[2])
        course_entry.insert(0, student[3])

# --- UI Setup ---
root = tk.Tk()
root.title("Student Management System")
root.geometry("550x420")

# LIGHT BROWN WINDOW BACKGROUND
root.configure(bg="#D2B48C")  # ← Light brown / Tan color

# STYLING — Table: light brown background + BLACK text inside
style = ttk.Style(root)
style.configure(
    "Treeview",
    background="#DECBA8",       # Lighter brown table background
    foreground="#000000",       # BLACK text inside table
    fieldbackground="#DECBA8",
    rowheight=25
)
style.configure(
    "Treeview.Heading",
    background="#8B5A2B",       # Darker brown header
    foreground="#000000",       # White text on header
    font=("Arial", 10, "bold")
)
style.map(
    "Treeview",
    background=[("selected", "#C49A6C")],  # Medium brown when selected
    foreground=[("selected", "#000000")]   # Black text when selected
)

# Labels & Entries
tk.Label(root, text="Name", bg="#D2B48C").grid(row=0, column=0, padx=15, pady=12, sticky="e")
name_entry = tk.Entry(root, width=35)
name_entry.grid(row=0, column=1, padx=15, pady=12)

tk.Label(root, text="Age", bg="#D2B48C").grid(row=1, column=0, padx=15, pady=8, sticky="e")
age_entry = tk.Entry(root, width=35)
age_entry.grid(row=1, column=1, padx=15, pady=8)

tk.Label(root, text="Course", bg="#D2B48C").grid(row=2, column=0, padx=15, pady=8, sticky="e")
course_entry = tk.Entry(root, width=35)
course_entry.grid(row=2, column=1, padx=15, pady=8)

# Buttonss
tk.Button(root, text="Add", command=add_student, width=12).grid(row=3, column=0, padx=8, pady=12)
tk.Button(root, text="Update", command=update_student, width=12).grid(row=3, column=1, padx=8, pady=12)
tk.Button(root, text="Delete", command=delete_student, width=12).grid(row=3, column=2, padx=8, pady=12)
tk.Button(root, text="Clear", command=clear_fields, width=12).grid(row=3, column=3, padx=8, pady=12)

# Table / Treeview
columns = ("id", "name", "age", "course")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10, style="Treeview")
tree.heading("id", text="ID")
tree.heading("name", text="Name")
tree.heading("age", text="Age")
tree.heading("course", text="Course")

tree.column("id", width=55)
tree.column("name", width=160)
tree.column("age", width=70)
tree.column("course", width=200)

tree.grid(row=4, column=0, columnspan=4, padx=15, pady=5)
tree.bind("<<TreeviewSelect>>", select_student)

display_students()
root.mainloop()
