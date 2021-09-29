from cowpy import cow
from flask import Flask, Response
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    message = cow.Cowacter().milk('Hello from Python from a Serverless Function!')
    return Response(f"<pre>{message}</pre>", mimetype="text/html")

