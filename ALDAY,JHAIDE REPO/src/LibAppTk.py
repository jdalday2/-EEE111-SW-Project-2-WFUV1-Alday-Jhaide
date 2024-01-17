from LibDb import LibDb
from LibGuiTk import LibGuiTk

def main():
    db = LibDb(init=False, dbName='LibDb.csv')
    app = LibGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()