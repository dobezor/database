import sqlite3
import tkinter as tk
from tkinter import filedialog, ttk


db_file_path = None

def view_table():
    global db_file_path


    db_file_path = filedialog.askopenfilename(filetypes=[("SQLite databases", "*.db")])

    if db_file_path:
        try:

            conn = sqlite3.connect(db_file_path)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()


            for row in table_tree.get_children():
                table_tree.delete(row)


            for table in tables:
                table_tree.insert("", "end", values=(table[0],))

            conn.close()

        except sqlite3.Error as e:
            result_label.config(text="Ошибка при работе с базой данных: " + str(e))
    else:
        result_label.config(text="Файл не выбран.")

def view_table_contents(event):
    global db_file_path


    if not table_tree.selection():

        return

    selected_item = table_tree.selection()[0]
    table_name = table_tree.item(selected_item)["values"][0]

    if db_file_path:
        try:

            conn = sqlite3.connect(db_file_path)
            cursor = conn.cursor()


            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()


            for row in table_contents_tree.get_children():
                table_contents_tree.delete(row)


            columns = [description[0] for description in cursor.description]
            table_contents_tree["columns"] = columns
            table_contents_tree.heading("#0", text="ID")
            for col in columns:
                table_contents_tree.heading(col, text=col)


            for i, row in enumerate(rows):
                table_contents_tree.insert("", "end", iid=i+1, text=str(i+1), values=row)

            conn.close()
            result_label.config(text=f"Таблица '{table_name}' успешно загружена.")

        except sqlite3.OperationalError:
            result_label.config(text="Ошибка: Таблица не найдена.")
        except sqlite3.Error as e:
            result_label.config(text="Ошибка при работе с базой данных: " + str(e))
    else:
        result_label.config(text="Файл базы данных не выбран.")


root = tk.Tk()
root.title("Просмотр файлов .db")


open_button = tk.Button(root, text="Выбрать файл .db", command=view_table)
open_button.pack(pady=10)


table_tree = ttk.Treeview(root, columns=("Таблицы",))
table_tree.heading("#0", text="Таблицы")
table_tree.bind("<<TreeviewSelect>>", view_table_contents)
table_tree.pack(fill="both", expand=True, padx=10, pady=5)


table_contents_tree = ttk.Treeview(root)
table_contents_tree.pack(fill="both", expand=True, padx=10, pady=5)


result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
