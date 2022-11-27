import sqlite3

from app import app, connect_db


def create_db():
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

class FDataBase:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()

    def delMenu(self, id=0):
        try:
            if id == 0:
                 self.__cur.execute(f"DELETE FROM mainmenu ")
            else:
                 self.__cur.execute(f"DELETE FROM mainmenu WHERE id=={id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления в базу данных',str(e))
            return False
        return True
    def addMenu(self,title,url):
        try:
            if id == 0:
                self.__cur.execute(f"INSERT INTO POST VALUES(null,?,?)", (title, url))
            else:
                self.__db.commit()
            except sqlite3.Error as e:
            print('Ошибка добавления в базу данных', str(e))
            return False
        return True




if __name__ == '__main__':
    print(create_db.__doc__)
    db = connect_db()
    db = FDataBase(db)
    print(db.addMenu('Главная','index'))
    #print(db.addMenu('Регистрация', 'login_2var'))
    #print(db.addMenu('Неизвестная страница', 'page404'))
    #print(db.addMenu('Ошибка при регистрации', 'errlog'))
    #print(db.addMenu('База', 'base'))
    #print(db.addMenu('Регистрация', 'login_2var'))
    #print(db.delMenu(0))


