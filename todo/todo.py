# -*- coding: utf-8 -*-
# todo/todo.py

from flask import Flask
from flask import g
from flask import render_template
from flask import flash, redirect, url_for, request

from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY = 'bardzosekretnawartosc',
    DATABASE = os.path.join(app.root_path, 'db.sqlite'),
    SITE_NAME = 'Moje zadania'
))

def connect_db():
    """Nawiazywanie połaczenia z bazą danych określoną w konfiguracji"""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Funkcja pomocnicza tworząca połączenie z bazą danych"""
    if not hasattr(g, 'db'): # jeżeli brak połączenia, to je tworzymy
        g.db = connect_db()
    return g.db # zwracamy połączenie z bazą

@app.teardown_request
def close_db(error):
    """Zamykanie połączenia z bazą"""
    if hasattr(g, 'db'):
        g.db.close()





@app.route('/', methods=['POST', 'GET'])
def index():

    error = None

    if request.method == 'POST':
        if len(request.form['zadanie']) > 0:
            zadanie = request.form['zadanie']
            zrobione = 0
            data_pub = datetime.now()
            db=get_db()
            db.execute('insert into zadania (zadanie, zrobione, data_pub) values (?, ?, ?);',
                        [zadanie, zrobione, data_pub])
            db.commit()
            return redirect(url_for('index'))
        error = u'Nie moża dodać pustego zadania'


    db = get_db()
    kursor  = db.execute('select * from zadania order by data_pub desc;')
    zadania = kursor.fetchall()
    return render_template('zadania_lista.html', zadania=zadania, error=error)



if __name__ == '__main__':
    app.run(debug=True)