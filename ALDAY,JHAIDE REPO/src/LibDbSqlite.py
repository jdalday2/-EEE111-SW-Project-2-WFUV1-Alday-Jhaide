'''
This is the interface to an SQLite Database
'''

import sqlite3

class LibDbSqlite:
    def __init__(self, dbName='Books.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                isbn TEXT PRIMARY KEY,
                title TEXT,
                genre TEXT,
                publication TEXT,
                availability TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Books (
                    isbn TEXT PRIMARY KEY,
                    title TEXT,
                    genre TEXT,
                    publication TEXT,
                    availability TEXT)''')
        self.commit_close()

    def fetch_books(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Books')
        books =self.cursor.fetchall()
        self.conn.close()
        return books

    def insert_book(self, isbn, title, genre, publication, availability):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Books (isbn, title, genre, publication, availability) VALUES (?, ?, ?, ?, ?)',
                    (isbn, title, genre, publication, availability))
        self.commit_close()

    def delete_book(self, isbn):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Books WHERE isbn = ?', (isbn,))
        self.commit_close()

    def update_book(self, new_title, new_genre, new_publication, new_availability, isbn):
        self.connect_cursor()
        self.cursor.execute('UPDATE Books SET title = ?, genre = ?, publication = ?, availability = ? WHERE isbn = ?',
                    (new_title, new_genre, new_publication, new_availability, isbn))
        self.commit_close()

    def isbn_exists(self, isbn):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Books WHERE isbn = ?', (isbn,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_books()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

def test_LibDb():
    iLibDb = LibDbSqlite(dbName='LibDbSql.db')

    for entry in range(30):
        iLibDb.insert_book(entry, f'ISBN{entry} Title{entry}', f'Genre {entry}', 'Publication', 'Availability')
        assert iLibDb.isbn_exists(entry)

    all_entries = iLibDb.fetch_books()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iLibDb.update_book(f'ISBN{entry} Title{entry}', f'Genre {entry}', 'Publication', 'Availability', entry)
        assert iLibDb.isbn_exists(entry)

    all_entries = iLibDb.fetch_books()
    assert len(all_entries) == 30

    for entry in range(10):
        iLibDb.delete_book(entry)
        assert not iLibDb.isbn_exists(entry) 

    all_entries = iLibDb.fetch_books()
    assert len(all_entries) == 20