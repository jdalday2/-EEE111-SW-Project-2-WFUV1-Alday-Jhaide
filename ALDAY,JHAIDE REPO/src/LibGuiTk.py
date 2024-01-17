from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from LibDbSqlite import LibDbSqlite

class LibGuiTk(Tk):

    def __init__(self, dataBase=LibDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Library Management System')
        self.geometry('1500x500')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'ISBN' Label and Entry Widgets
        self.isbn_label = self.newCtkLabel('ISBN')
        self.isbn_label.place(x=20, y=40)
        self.isbn_entryVar = StringVar()
        self.isbn_entry = self.newCtkEntry(entryVariable=self.isbn_entryVar)
        self.isbn_entry.place(x=100, y=40)

        # 'Title' Label and Entry Widgets
        self.title_label = self.newCtkLabel('Title')
        self.title_label.place(x=20, y=100)
        self.title_entryVar = StringVar()
        self.title_entry = self.newCtkEntry(entryVariable=self.title_entryVar)
        self.title_entry.place(x=100, y=100)

        # 'Genre' Label and Combo Box Widgets
        self.genre_label = self.newCtkLabel('Genre')
        self.genre_label.place(x=20, y=160)
        self.genre_cboxVar = StringVar()
        self.genre_cboxOptions = ['Fiction', 'Non-Fiction', 'Mystery', 'Science Fiction', 'Fantasy', 'Romance', 'Thriller', 'Horror', 'Historical Fiction', 'Biography','Science','Philosophy','Psychology','Technology','Business','Education','Travel']
        self.genre_cbox = self.newCtkComboBox(options=self.genre_cboxOptions, 
                                    entryVariable=self.genre_cboxVar)
        self.genre_cbox.place(x=100, y=160)

        # 'Publication' Label and Combo Box Widgets
        self.publication_label = self.newCtkLabel('Publication')
        self.publication_label.place(x=20, y=220)
        self.publication_cboxVar = StringVar()
        self.publication_cboxOptions = ['2000', '2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']
        self.publication_cbox = self.newCtkComboBox(options=self.publication_cboxOptions, 
                                    entryVariable=self.publication_cboxVar)
        self.publication_cbox.place(x=100, y=220)

        # 'Availability' Label and Combo Box Widgets
        self.availability_label = self.newCtkLabel('Availability')
        self.availability_label.place(x=20, y=280)
        self.availability_cboxVar = StringVar()
        self.availability_cboxOptions = ['Available', 'Checked Out', 'On Hold', 'Not Available']
        self.availability_cbox = self.newCtkComboBox(options=self.availability_cboxOptions, 
                                    entryVariable=self.availability_cboxVar)
        self.availability_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Book',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Book',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Book',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Delete Book',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=670,y=400)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=980,y=400)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('ISBN', 'Title', 'Genre', 'Publication', 'Availability')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ISBN', anchor=tk.CENTER, width=10)
        self.tree.column('Title', anchor=tk.CENTER, width=150)
        self.tree.column('Genre', anchor=tk.CENTER, width=150)
        self.tree.column('Publication', anchor=tk.CENTER, width=10)
        self.tree.column('Availability', anchor=tk.CENTER, width=150)

        self.tree.heading('ISBN', text='ISBN')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Publication', text='Publication')
        self.tree.heading('Availability', text='Availability')

        self.tree.place(x=360, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, 
                        text=text)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        
        # set default value to 1st option
        widget['values'] = tuple(options)
        widget.current(1)
        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
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
        self.isbn_entryVar.set('')
        self.title_entryVar.set('')
        self.genre_cboxVar.set('SW-Engineer')
        self.publication_cboxVar.set('Male')
        self.availability_cboxVar.set('On-Site')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.isbn_entryVar.set(row[0])
            self.title_entryVar.set(row[1])
            self.genre_cboxVar.set(row[2])
            self.publication_cboxVar.set(row[3])
            self.availability_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        isbn=self.isbn_entryVar.get()
        title=self.title_entryVar.get()
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
            isbn = self.isbn_entryVar.get()
            self.db.delete_book(isbn)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a book to update')
        else:
            isbn=self.isbn_entryVar.get()
            title=self.title_entryVar.get()
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





