import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")

        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.setup_ui()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                id INTEGER PRIMARY KEY,
                                title TEXT,
                                author TEXT,
                                year INTEGER,
                                copies INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                email TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
                                id INTEGER PRIMARY KEY,
                                book_id INTEGER,
                                user_id INTEGER,
                                loan_date TEXT,
                                return_date TEXT,
                                returned INTEGER,
                                FOREIGN KEY(book_id) REFERENCES books(id),
                                FOREIGN KEY(user_id) REFERENCES users(id))''')
        self.conn.commit()

    def setup_ui(self):
        # UI para registrar livros
        tk.Label(self.root, text="Título do Livro").grid(row=0, column=0)
        self.book_title_entry = tk.Entry(self.root)
        self.book_title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Autor do Livro").grid(row=1, column=0)
        self.book_author_entry = tk.Entry(self.root)
        self.book_author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Ano de Publicação").grid(row=2, column=0)
        self.book_year_entry = tk.Entry(self.root)
        self.book_year_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Números de Cópias").grid(row=3, column=0)
        self.book_copies_entry = tk.Entry(self.root)
        self.book_copies_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Registrar Livro", command=self.register_book).grid(row=4, column=0, columnspan=2)

        # UI para registrar usuários
        tk.Label(self.root, text="Nome do Usuário").grid(row=5, column=0)
        self.user_name_entry = tk.Entry(self.root)
        self.user_name_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Email do Usuário").grid(row=6, column=0)
        self.user_email_entry = tk.Entry(self.root)
        self.user_email_entry.grid(row=6, column=1)

        tk.Button(self.root, text="Registrar Usuário", command=self.register_user).grid(row=7, column=0, columnspan=2)

        # UI para empréstimos
        tk.Label(self.root, text="ID do Livro").grid(row=8, column=0)
        self.loan_book_id_entry = tk.Entry(self.root)
        self.loan_book_id_entry.grid(row=8, column=1)

        tk.Label(self.root, text="ID do Usuário").grid(row=9, column=0)
        self.loan_user_id_entry = tk.Entry(self.root)
        self.loan_user_id_entry.grid(row=9, column=1)

        tk.Button(self.root, text="Empréstimo de Livro", command=self.loan_book).grid(row=10, column=0, columnspan=2)

        # UI para devoluções
        tk.Label(self.root, text="ID do Empréstimo").grid(row=11, column=0)
        self.return_loan_id_entry = tk.Entry(self.root)
        self.return_loan_id_entry.grid(row=11, column=1)

        tk.Button(self.root, text="Devolução de Livro", command=self.return_book).grid(row=12, column=0, columnspan=2)

        # UI para consultar livros
        tk.Label(self.root, text="Consultar Livro por:").grid(row=13, column=0)
        self.search_type = tk.StringVar(value="Título")
        tk.Radiobutton(self.root, text="Título", variable=self.search_type, value="Título").grid(row=13, column=1)
        tk.Radiobutton(self.root, text="Autor", variable=self.search_type, value="Autor").grid(row=13, column=2)
        tk.Radiobutton(self.root, text="Ano de Publicação", variable=self.search_type, value="Ano").grid(row=13, column=3)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=14, column=1)

        tk.Button(self.root, text="Consultar", command=self.consult_books).grid(row=14, column=2)

        # UI para gerar relatório
        tk.Button(self.root, text="Relatório", command=self.generate_report).grid(row=15, column=0, columnspan=4)

    def register_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        year = int(self.book_year_entry.get())
        copies = int(self.book_copies_entry.get())
        self.cursor.execute("INSERT INTO books (title, author, year, copies) VALUES (?, ?, ?, ?)", (title, author, year, copies))
        self.conn.commit()
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)
        self.book_copies_entry.delete(0, tk.END)
        messagebox.showinfo("Info", "Livro registrado com sucesso")

    def register_user(self):
        name = self.user_name_entry.get()
        email = self.user_email_entry.get()
        self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()
        self.user_name_entry.delete(0, tk.END)
        self.user_email_entry.delete(0, tk.END)
        messagebox.showinfo("Info", "Usuário registrado com sucesso")

    def loan_book(self):
        book_id = int(self.loan_book_id_entry.get())
        user_id = int(self.loan_user_id_entry.get())
        self.cursor.execute("SELECT copies FROM books WHERE id=?", (book_id,))
        copies = self.cursor.fetchone()[0]
        if copies > 0:
            self.cursor.execute("INSERT INTO loans (book_id, user_id, loan_date, return_date, returned) VALUES (?, ?, ?, ?, ?)",
                                (book_id, user_id, datetime.now().strftime("%Y-%m-%d"), None, 0))
            self.cursor.execute("UPDATE books SET copies=copies-1 WHERE id=?", (book_id,))
            self.conn.commit()
            self.loan_book_id_entry.delete(0, tk.END)
            self.loan_user_id_entry.delete(0, tk.END)
            messagebox.showinfo("Info", "Livro emprestado com sucesso")
        else:
            messagebox.showwarning("Erro", "Livro não disponível para empréstimo")

    def return_book(self):
        loan_id = int(self.return_loan_id_entry.get())
        self.cursor.execute("UPDATE loans SET return_date=?, returned=1 WHERE id=?", (datetime.now().strftime("%Y-%m-%d"), loan_id))
        self.cursor.execute("SELECT book_id FROM loans WHERE id=?", (loan_id,))
        book_id = self.cursor.fetchone()[0]
        self.cursor.execute("UPDATE books SET copies=copies+1 WHERE id=?", (book_id,))
        self.conn.commit()
        self.return_loan_id_entry.delete(0, tk.END)
