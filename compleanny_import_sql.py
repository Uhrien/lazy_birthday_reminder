import sqlite3
import locale
from datetime import datetime

# Impostazione della localizzazione italiana
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

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

# Funzione per importare i compleanni dal file
def import_birthdays(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    conn = sqlite3.connect('compleanni.db')
    cur = conn.cursor()

    for line in lines:
        line = line.strip()
        if '->' in line:
            date_part, names_part = line.split('->')
            date_part = date_part.strip()
            names = [name.strip() for name in names_part.split(',')]
            # Converti la data nel formato "mese-giorno"
            datetime_part = datetime.strptime(date_part, '%d %B').strftime('%m-%d')
            for name in names:
                cur.execute('INSERT INTO Compleanni (data, nome, datetime) VALUES (?, ?, ?)', 
                            (date_part, name, datetime_part))

    conn.commit()
    conn.close()

# Creazione della tabella nel database
create_table()

# Importazione dei compleanni dal file
import_birthdays('Compleanni.txt')
