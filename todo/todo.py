# -*- coding: utf-8 -*-
# todo/todo.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Pierwszy commit na poważnie'

if __name__ == '__main__':
    app.run(debug=True)