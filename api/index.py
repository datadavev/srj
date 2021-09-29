from cowpy import cow
from flask import Flask, Response
import sqlite3

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    msg = []
    for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        msg.append(str(row))
    message = cow.Cowacter().milk('Hello from Python from a simple Serverless Function!')
    return Response(f"<pre>{message}\n{'|'.join(msg)}</pre>", mimetype="text/html")

