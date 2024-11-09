import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class LibrarySystem:

    def __init__(self, root):
        # criação do banco de dados usando sqlite
        self.root = root
        self.root.title("Library System")

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
        # Registrar livro
        tk.Label(self.root, text="Título do Livro").grid(row=0, column=0)
        self.book_title_entry = tk.Entry(self.root)
        self.book_title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Autor do Livro").grid(row=1, column=0)
        self.book_author_entry = tk.Entry(self.root)
        self.book_author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Ano de Publicação").grid(row=2, column=0)
        self.book_year_entry = tk.Entry(self.root)
        self.book_year_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Número de Cópias").grid(row=3, column=0)
        self.book_copies_entry = tk.Entry(self.root)
        self.book_copies_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Registrar Livro", command=self.register_book).grid(row=4, column=0, columnspan=2)

        # Registrar usuário
        tk.Label(self.root, text="Nome do Usuário").grid(row=5, column=0)
        self.user_name_entry = tk.Entry(self.root)
        self.user_name_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Email do Usuário").grid(row=6, column=0)
        self.user_email_entry = tk.Entry(self.root)
        self.user_email_entry.grid(row=6, column=1)

        tk.Button(self.root, text="Registrar Usuário", command=self.register_user).grid(row=7, column=0, columnspan=2)

        # Empréstimo
        tk.Label(self.root, text="ID do Livro").grid(row=8, column=0)
        self.loan_book_id_entry = tk.Entry(self.root)
        self.loan_book_id_entry.grid(row=8, column=1)

        tk.Label(self.root, text="ID do Usuário").grid(row=9, column=0)
        self.loan_user_id_entry = tk.Entry(self.root)
        self.loan_user_id_entry.grid(row=9, column=1)

        tk.Button(self.root, text="Empréstimo de Livro", command=self.loan_book).grid(row=10, column=0, columnspan=2)

        # Devolução
        tk.Label(self.root, text="ID do Empréstimo").grid(row=11, column=0)
        self.return_loan_id_entry = tk.Entry(self.root)
        self.return_loan_id_entry.grid(row=11, column=1)

        tk.Button(self.root, text="Devolução de Livro", command=self.return_book).grid(row=12, column=0, columnspan=2)

        # Consultar livros
        tk.Button(self.root, text="Consultar Livros", command=self.consult_books).grid(row=13, column=0, columnspan=2)

        # Relátorio
        tk.Button(self.root, text="Relatório", command=self.generate_report).grid(row=14, column=0, columnspan=2)

    def register_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        year = int(self.book_year_entry.get())
        copies = int(self.book_copies_entry.get())
        self.cursor.execute("INSERT INTO books (title, author, year, copies) VALUES (?, ?, ?, ?)", (title, author, year, copies))
        self.conn.commit()
        self.clear_entries("book")
        messagebox.showinfo("Info", "Livro registrado com sucesso")

    def register_user(self):
        name = self.user_name_entry.get()
        email = self.user_email_entry.get()
        self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()
        self.clear_entries("user")
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
            self.clear_entries("loan")
            messagebox.showinfo("Info", "Livro emprestado com sucesso")
        else:
            messagebox.showwarning("Erro", "Livro não disponível")

    def return_book(self):
        loan_id = int(self.return_loan_id_entry.get())
        self.cursor.execute("UPDATE loans SET return_date=?, returned=1 WHERE id=?", (datetime.now().strftime("%Y-%m-%d"), loan_id))
        self.cursor.execute("SELECT book_id FROM loans WHERE id=?", (loan_id,))
        book_id = self.cursor.fetchone()[0]
        self.cursor.execute("UPDATE books SET copies=copies+1 WHERE id=?", (book_id,))
        self.conn.commit()
        self.clear_entries("return")
        messagebox.showinfo("Info", "Livro devolvido com sucesso")

    def consult_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        display_text = "ID | Título | Autor | Ano | Cópias\n"
        display_text += "-"*50 + "\n"
        for book in books:
            display_text += f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]}\n"
        messagebox.showinfo("Consulta de Livros", display_text)

    def generate_report(self):
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total_books = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE copies>0")
        available_books = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM loans WHERE returned=0")
        borrowed_books = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM users")
        total_users = self.cursor.fetchone()[0]

        report_text = f"Total de Livros Registrados: {total_books}\n"
        report_text += f"Livros Disponíveis: {available_books}\n"
        report_text += f"Livros Emprestados: {borrowed_books}\n"
        report_text += f"Usuários Registrados: {total_users}"
        messagebox.showinfo("Relatório", report_text)

    def clear_entries(self, type_):
        if type_ == "book":
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
            self.book_year_entry.delete(0, tk.END)
            self.book_copies_entry.delete(0, tk.END)
        elif type_ == "user":
            self.user_name_entry.delete(0, tk.END)
            self.user_email_entry.delete(0, tk.END)
        elif type_ == "loan":
            self.loan_book_id_entry.delete(0, tk.END)
            self.loan_user_id_entry.delete(0, tk.END)
        elif type_ == "return":
            self.return_loan_id_entry.delete(0, tk.END)

    def __del__(self):
        self.conn.close()

# Criando a janela principal
root = tk.Tk()
app = LibrarySystem(root)
root.mainloop()
