import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
import locale
from datetime import datetime

# Impostazione della localizzazione italiana
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

# Funzione ausiliaria per convertire il nome del mese in maiuscolo
def capitalize_month_name(date_str):
    parts = date_str.split()
    if len(parts) == 2:
        day = parts[0]
        month = parts[1].capitalize()
        return f"{day} {month}"
    return date_str

# Funzione per creare la tabella dei compleanni
def create_table():
    conn = sqlite3.connect('compleanni.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Compleanni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        nome TEXT NOT NULL,
        datetime TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Funzione per salvare il compleanno nel database
def save_birthday():
    date = cal.get_date()
    formatted_date = date.strftime('%d %B')
    formatted_date = capitalize_month_name(formatted_date)  # Converti nome del mese in maiuscolo
    datetime_part = date.strftime('%m-%d')  # Formato mese-giorno
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Input Error", "Il nome non può essere vuoto!")
        return
    conn = sqlite3.connect('compleanni.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO Compleanni (data, nome, datetime) VALUES (?, ?, ?)', 
                (formatted_date, name, datetime_part))
    conn.commit()
    conn.close()
    name_entry.delete(0, tk.END)
    messagebox.showinfo("Successo", "Compleanno salvato!")
    refresh_records()

# Funzione per aggiornare la lista dei compleanni
def refresh_records():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect('compleanni.db')
    cur = conn.cursor()
    cur.execute('SELECT data, nome FROM Compleanni ORDER BY datetime')
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# Creazione della tabella nel database
create_table()

# Creazione della finestra principale
root = tk.Tk()
root.title("Gestione Compleanni")

# Creazione della sezione di inserimento
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

tk.Label(input_frame, text="Data:").grid(row=0, column=0, padx=5, pady=5)
cal = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy', locale='it_IT')
cal.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=1, column=1, padx=5, pady=5)

save_button = tk.Button(input_frame, text="Salva", command=save_birthday)
save_button.grid(row=2, columnspan=2, pady=10)

# Creazione della sezione di visualizzazione
view_frame = tk.Frame(root)
view_frame.pack(padx=10, pady=10)

tree = ttk.Treeview(view_frame, columns=("Data", "Nome"), show='headings', height=20)
tree.heading("Data", text="Data")
tree.heading("Nome", text="Nome")
tree.pack(padx=10, pady=10)

# Aggiornamento iniziale dei record
refresh_records()

# Avvio del loop principale
root.mainloop()
