import os
import sqlite3

from flask import Flask
from flask_bcrypt import Bcrypt

DATABASE = 'database.db'
app = Flask(__name__)
bcrypt = Bcrypt(app)


def create():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()

    c.execute('''
        CREATE TABLE chatHist (
            itemid integer PRIMARY KEY AUTOINCREMENT,
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
