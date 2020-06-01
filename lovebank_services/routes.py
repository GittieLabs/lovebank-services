from flask import request
from lovebank_services import app    # import app from __init__.py

@app.route("/", methods=['GET'])
def hello():
    return "Hello, World!"
