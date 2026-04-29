import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.setup_ui()
        self.load_movies()

    def setup_ui(self):
        # Поля формы
        tk.Label(self.root, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Рейтинг (0–10)").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Title", "Genre", "Year", "Rating"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтрация по жанру
        tk.Label(self.root, text="Фильтр по жанру").grid(row=6, column=0, padx=5, pady=5)
        self.genre_filter = ttk.Combobox(self.root, values=[])
        self.genre_filter.grid(row=6, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Фильтровать по жанру", command=self.filter_by_genre).grid(row=7, column=0, pady=5)

        # Фильтрация по году
        tk.Label(self.root, text="Фильтр по году").grid(row=8, column=0, padx=5, pady=5)
        self.year_filter = tk.Entry(self.root)
        self.year_filter.grid(row=8, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Фильтровать по году", command=self.filter_by_year).grid(row=9, column=0, pady=5)

        # Сброс фильтра
        tk.Button(self.root, text="Сбросить фильтр", command=self.load_movies).grid(row=9, column=1, pady=5)

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()

        try:
            year = int(self.year_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        try:
            rating = float(self.rating_entry.get())
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.update_table()
        self.clear_entries()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in self.movies:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))
        genres = list(set([movie["genre"] for movie in self.movies]))
        self.genre_filter["values"] = genres

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def save_movies(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)

    def load_movies(self):
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)
        self.update_table()

    def filter_by_genre(self):
        genre = self.genre_filter.get()
        filtered = [m for m in self.movies if m["genre"] == genre]
        self.display_filtered(filtered)

    def filter_by_year(self):
        try:
            year = int(self.year_filter.get())
            filtered = [m for m in self.movies if m["year"] == year]
            self.display_filtered(filtered)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")

    def display_filtered(self, filtered_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for movie in filtered_list:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def on_closing(self):
        self.save_movies()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()