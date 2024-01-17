from LibDbEntry import LibDbEntry
import json
import csv
class LibDb:
    """
    - simple database to store LibDbEntry objects
    """    

    def __init__(self, init=False, dbName='LibDb.csv'):
        """
        - initialize database variables here
        - mandatory :
            - any type can be used to store database entries for LibDbEntry objects
            - e.g. list of class, list of dictionary, list of tuples, dictionary of tuples etc.
        """
        # CSV filename         
        self.dbName = dbName
        # initialize container of database entries
        self.entries = []
        print('TODO: __init__')


    def fetch_books(self):
        """
        - returns a list of tuples containing Book entry fields
    
        """
        print('TODO: fetch_books')
        tupleList = []

        # Append entries from self.entries to tupleList
        tupleList += [(entry.isbn, entry.title, entry.genre, entry.publication, entry.availability) for entry in self.entries]

        return tupleList

    def insert_book(self, isbn, title, genre, publication, availability):
        """
        - inserts an entry in the database
        - no return value
        """
        newEntry = LibDbEntry(isbn=isbn, title=title, genre=genre, publication=publication, availability=availability)
        self.entries.append(newEntry)
        print('TODO: insert_book')

    def delete_book(self, isbn):
        """
        - deletes the corresponding entry in the database as specified by 'isbn'
        - no return value
        """
        for entry in self.entries:
            if entry.isbn == isbn:
                self.entries.remove(entry)
        print('TODO: delete_book')

    def update_book(self, new_title, new_genre, new_publication, new_status, isbn):
        """
        - updates the corresponding entry in the database as specified by 'isbn'
        - no return value
        """
        for entry in self.entries:
            if entry.isbn == isbn:
                entry.title = new_title
                entry.genre = new_genre
                entry.publication = new_publication
                entry.availability = new_status
        print('TODO: update_book')     
              

    def export_csv(self):
        """
        - exports database entries as a CSV file
        - CSV : Comma Separated Values
        - no return value
        - example
        12,Eileen Dover,SW-Engineer,Male,On-Site
        13,Ann Chovey,HW-Engineer,Female,On-Site
        14,Chris P. Bacon,SW-Engineer,Male,On-Leave
        15,Russell Sprout,SW-Engineer,Male,Remote
        16,Oscar Lott,Project-Manager,Male,On-Site        
        """
        with open(self.dbName, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry.isbn},{entry.title},{entry.genre},{entry.publication},{entry.availability}\n")
        print('TODO: export_csv')

    def isbn_exists(self, isbn):
        """
        - returns True if an entry exists for the specified 'isbn'
        - else returns False
        """
        return any(entry.isbn == isbn for entry in self.entries)
    
    def export_json(self, json_filename='LibDb.json'):
        data = [{'ISBN': entry.isbn,
                 'Title': entry.title,
                 'Genre': entry.genre,
                 'Publication': entry.publication,
                 'Availability': entry.availability} for entry in self.entries]

        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def import_csv(self, csv_filename):
        try:
            if not csv_filename.lower().endswith('.csv'):
                csv_filename += '.csv'

            with open(csv_filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    book_isbn, book_title, book_genre, book_publication, book_availability = row
                    # Add logic to handle the data, e.g., insert into your database
                    self.insert_book(book_isbn, book_title, book_genre, book_publication, book_availability)
            print('Data imported successfully')
            return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {csv_filename}')
            return False
        except Exception as e:
            print(f'Error importing data: {e}')
            return False        

        