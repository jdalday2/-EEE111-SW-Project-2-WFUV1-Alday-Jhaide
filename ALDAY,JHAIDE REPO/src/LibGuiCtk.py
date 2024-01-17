import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from LibDbSqlite import LibDbSqlite
import json
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from LibDbSqlite import LibDbSqlite


class LibGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=LibDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Library Management System')
        self.geometry('1500x650')
        self.config(bg='#301919')
        self.resizable(False, False)

        self.font1 = ('Times New Roman', 20, 'bold')
        self.font2 = ('Times New Roman', 12, 'bold')

        # Data Entry Form
        # 'ISBN' Label and Entry Widgets
        self.isbn_label = self.newCtkLabel('ISBN')
        self.isbn_label.place(x=10, y=250)
        self.isbn_entry = self.newCtkEntry()
        self.isbn_entry.place(x=10, y=280)

        # 'Title' Label and Entry Widgets
        self.title_label = self.newCtkLabel('Title')
        self.title_label.place(x=10, y=310)
        self.title_entry = self.newCtkEntry()
        self.title_entry.place(x=10, y=340)

        # 'Genre' Label and Combo Box Widgets
        self.genre_label = self.newCtkLabel('Genre')
        self.genre_label.place(x=10, y=370)
        self.genre_cboxVar = StringVar()
        self.genre_cboxOptions = ['Fiction', 'Non-Fiction', 'Mystery', 'Science Fiction', 'Fantasy', 'Romance', 'Thriller', 'Horror', 'Historical Fiction', 'Biography','Science','Philosophy','Psychology','Technology','Business','Education','Travel']
        self.genre_cbox = self.newCtkComboBox(options=self.genre_cboxOptions, 
                                    entryVariable=self.genre_cboxVar)
        self.genre_cbox.place(x=10, y=400)

        # 'Publication' Label and Combo Box Widgets
        self.publication_label = self.newCtkLabel('Publication Year')
        self.publication_label.place(x=10, y=430)
        self.publication_cboxVar = StringVar()
        self.publication_cboxOptions = ['2000', '2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']
        self.publication_cbox = self.newCtkComboBox(options=self.publication_cboxOptions, 
                                    entryVariable=self.publication_cboxVar)
        self.publication_cbox.place(x=10, y=460)

        # 'Availability' Label and Combo Box Widgets
        self.availability_label = self.newCtkLabel('Availability')
        self.availability_label.place(x=10, y=490)
        self.availability_cboxVar = StringVar()
        self.availability_cboxOptions = ['Available', 'Checked Out', 'On Hold', 'Not Available']
        self.availability_cbox = self.newCtkComboBox(options=self.availability_cboxOptions, 
                                    entryVariable=self.availability_cboxVar)
        self.availability_cbox.place(x=10, y=520)


        self.add_button = self.newCtkButton(text='Add Book',
                                onClickHandler=self.add_entry,
                                fgColor='#38B873',
                                hoverColor='#34A668',
                                borderColor='#38B873')
        self.add_button.place(x=990,y=460)

        self.new_button = self.newCtkButton(text='New Book',
                                onClickHandler=lambda:self.clear_form(True),
                                fgColor='#925555',
                                hoverColor='#6D4242',
                                borderColor='#925555')
        self.new_button.place(x=450,y=460)

        self.update_button = self.newCtkButton(text='Update Book',
                                    onClickHandler=self.update_entry,
                                    fgColor='#925555',
                                    hoverColor='#6D4242',
                                    borderColor='#925555')
        self.update_button.place(x=450,y=520)

        self.delete_button = self.newCtkButton(text='Delete Book',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#DD0909',
                                    hoverColor='#BD0B0B',
                                    borderColor='#DD0909')
        self.delete_button.place(x=990,y=400)

        self.import_button = self.newCtkButton(text='Import from CSV',
                                    onClickHandler=self.import_from_csv,
                                    fgColor='#925555',
                                    hoverColor='#6D4242',
                                    borderColor='#925555')
        self.import_button.place(x=720,y=460)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv,
                                    fgColor='#925555',
                                    hoverColor='#6D4242',
                                    borderColor='#925555')
        self.export_button.place(x=990,y=520)

        self.export_json_button = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_entries_to_json,
                                    fgColor='#925555',
                                    hoverColor='#6D4242',
                                    borderColor='#925555')
        self.export_json_button.place(x=720,y=520)


        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#FFF',
                        background='#CFAC76',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('ISBN', 'Title', 'Genre', 'Publication', 'Availability')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ISBN', anchor=tk.CENTER, width=10)
        self.tree.column('Title', anchor=tk.CENTER, width=100)
        self.tree.column('Genre', anchor=tk.CENTER, width=100)
        self.tree.column('Publication', anchor=tk.CENTER, width=10)
        self.tree.column('Availability', anchor=tk.CENTER, width=100)

        self.tree.heading('ISBN', text='ISBN')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Publication', text='Publication')
        self.tree.heading('Availability', text='Availability')

        self.tree.place(x=192, y=10, width=1115, height=260)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#301919'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFBBBB'
        widget_BorderColor='#291616'
        widget_BorderWidth=1
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFBBBB'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#291616'
        widget_BorderWidth=1
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#301919', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        books = self.db.fetch_books()
        self.tree.delete(*self.tree.get_children())
        for book in books:
            print(book)
            self.tree.insert('', END, values=book)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.isbn_entry.delete(0, END)
        self.title_entry.delete(0, END)
        self.genre_cboxVar.set('Fiction')
        self.publication_cboxVar.set('2000')
        self.availability_cboxVar.set('Available')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.isbn_entry.insert(0, row[0])
            self.title_entry.insert(0, row[1])
            self.genre_cboxVar.set(row[2])
            self.publication_cboxVar.set(row[3])
            self.availability_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        isbn=self.isbn_entry.get()
        title=self.title_entry.get()
        genre=self.genre_cboxVar.get()
        publication=self.publication_cboxVar.get()
        availability=self.availability_cboxVar.get()

        if not (isbn and title and genre and publication and availability):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.isbn_exists(isbn):
            messagebox.showerror('Error', 'ISBN already exists')
        else:
            self.db.insert_book(isbn, title, genre, publication, availability)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a book to delete')
        else:
            isbn = self.isbn_entry.get()
            self.db.delete_book(isbn)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a book to update')
        else:
            isbn=self.isbn_entry.get()
            title=self.title_entry.get()
            genre=self.genre_cboxVar.get()
            publication=self.publication_cboxVar.get()
            availability=self.availability_cboxVar.get()
            self.db.update_book(title, genre, publication, availability, isbn)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", ".csv")])

        if not file_path:
            messagebox.showinfo('Info', 'No file selected.')
            return

        if self.db.import_csv(file_path):
            messagebox.showinfo('Success', f'Data imported from {file_path}')
            # Optionally, update the displayed data in your GUI after importing
            self.add_to_treeview()
        else:
            messagebox.showerror('Error', f'Failed to import data from {file_path}')

    def export_entries_to_json(self):
        books = self.db.fetch_books()
        json_data = []

        for book in books:
            book_dict = {
                'ISBN': book[0],
                'Title': book[1],
                'Genre': book[2],
                'Publication': book[3],
                'Availability': book[4]
            }
            json_data.append(book_dict)

        # Export to JSON file
        with open('Books.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        messagebox.showinfo('Success', 'Data exported to Books.json')    





