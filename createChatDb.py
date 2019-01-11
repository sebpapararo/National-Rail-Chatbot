import os
import sqlite3

from flask import Flask

DATABASE = 'database.db'
app = Flask(__name__)


def create():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute('''
        CREATE TABLE chatHist (
            itemid integer PRIMARY KEY AUTOINCREMENT,
            whosaid varchar,
            item varchar
        );
    ''')

    db.commit()


def delete_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)


if __name__ == '__main__':
    delete_db()
    create()
