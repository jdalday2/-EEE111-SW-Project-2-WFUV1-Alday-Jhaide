from LibDb import LibDb
from LibGuiCtk import LibGuiCtk

def main():
    db = LibDb(init=False, dbName='LibDb.csv')
    app = LibGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()