from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Dean, I have demon blood in me!'