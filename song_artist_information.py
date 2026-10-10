import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("song_artist_information.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_title TEXT NOT NULL,
        artist_name TEXT NOT NULL,
        age INTEGER,
        genre TEXT
        )
    """)
conn.commit()
conn.close()

def create(song_title, artist_name, age, genre):
    conn = sqlite3.connect("song_artist_information.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO songs VALUES (NULL, ?, ?, ?, ?)",
        (song_title, artist_name, age, genre)
    )
    conn.commit()
    conn.close()
    return True

def read():
    conn = sqlite3.connect("song_artist_information.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    records = cursor.fetchall()
    conn.close()
    return records

def update(record_id, song_title, artist_name, age, genre):
    conn = sqlite3.connect("song_artist_information.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE songs SET song_title=?, artist_name=?, age=?, genre=? WHERE id=?",
        (song_title, artist_name, age, genre, record_id)
    )
    conn.commit()
    conn.close()
    return True

def delete(record_id):
    conn = sqlite3.connect("song_artist_information.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM songs WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    return True

def init_db():
    pass

class Song:
    def __init__(self, root):
        self.root = root
        self.root.title("Song & Artist CRUD System")
        self.root.geometry("700x450")
        self.selected_id = None

        input_frame = ttk.LabelFrame(root, text="Song Information")
        input_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(input_frame, text="Song Title:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.song_entry = ttk.Entry(input_frame, width=40)
        self.song_entry.grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(input_frame, text="Artist Name:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.artist_entry = ttk.Entry(input_frame, width=40)
        self.artist_entry.grid(row=1, column=1, padx=5, pady=8)

        ttk.Label(input_frame, text="Age:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.age_entry = ttk.Entry(input_frame, width=40)
        self.age_entry.grid(row=2, column=1, padx=5, pady=8)

        ttk.Label(input_frame, text="Genre:").grid(row=3, column=0, padx=5, pady=8, sticky="w")
        self.genre_entry = ttk.Entry(input_frame, width=40)
        self.genre_entry.grid(row=3, column=1, padx=5, pady=8)

        btn_frame = ttk.Frame(root)
        btn_frame.pack(padx=10, pady=5, fill="x")

        self.add_btn = ttk.Button(btn_frame, text="Add New", command=self.add)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.update_btn = ttk.Button(btn_frame, text="Update Selected", command=self.update, state="disabled")
        self.update_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = ttk.Button(btn_frame, text="Delete Selected", command=self.delete, state="disabled")
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="Clear Fields", command=self.clear)
        self.clear_btn.grid(row=0, column=3, padx=5)

        table_frame = ttk.LabelFrame(root, text="Records")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("ID", "Song Title", "Artist", "Age", "Genre")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.bind("<<TreeviewSelect>>", self.select)
        self.tree.pack(fill="both", expand=True)

        init_db()
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in read():
            self.tree.insert("", tk.END, values=record)

    def add(self):
        song = self.song_entry.get().strip()
        artist = self.artist_entry.get().strip()
        age_text = self.age_entry.get().strip()
        genre = self.genre_entry.get().strip()

        if not song or not artist:
            messagebox.showwarning("Warning", "Song Title and Artist Name are required!")
            return

        age = None
        if age_text:
            try:
                age = int(age_text)
            except ValueError:
                messagebox.showwarning("Warning", "Age must be a number!")
                return

        create(song, artist, age, genre)
        messagebox.showinfo("Success", "Record added!")
        self.clear()
        self.refresh_table()

    def select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            data = item["values"]
            self.selected_id = data[0]
            self.song_entry.delete(0, tk.END)
            self.song_entry.insert(0, data[1])
            self.artist_entry.delete(0, tk.END)
            self.artist_entry.insert(0, data[2])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, data[3] if data[3] else "")
            self.genre_entry.delete(0, tk.END)
            self.genre_entry.insert(0, data[4] if data[4] else "")
            self.update_btn.config(state="normal")
            self.delete_btn.config(state="normal")
        else:
            self.update_btn.config(state="disabled")
            self.delete_btn.config(state="disabled")

    def update(self):
        if not self.selected_id:
            return
        song = self.song_entry.get().strip()
        artist = self.artist_entry.get().strip()
        age_text = self.age_entry.get().strip()
        genre = self.genre_entry.get().strip()

        if not song or not artist:
            messagebox.showwarning("Warning", "Song Title and Artist Name are required!")
            return

        age = None
        if age_text:
            try:
                age = int(age_text)
            except ValueError:
                messagebox.showwarning("Warning", "Age must be a number!")
                return

        update(self.selected_id, song, artist, age, genre)
        messagebox.showinfo("Success", "The Record is updated!")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            return
        if messagebox.askyesno("Confirm", "Delete this record?"):
            delete(self.selected_id)
            messagebox.showinfo("Deleted", "Record removed!")
            self.clear()
            self.refresh_table()

    def clear(self):
        self.song_entry.delete(0, tk.END)
        self.artist_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.selected_id = None
        self.update_btn.config(state="disabled")
        self.delete_btn.config(state="disabled")
        self.tree.selection_remove(self.tree.selection())

if __name__ == "__main__":
    root = tk.Tk()
    app = Song(root)
    root.mainloop()
