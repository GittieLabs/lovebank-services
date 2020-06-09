from flask import Flask, request, jsonify

''' simple flask API example for example_pytest_test to use '''

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'

@app.route('/add', methods=['POST'])
def add():
 data = request.get_json()
 return jsonify({'sum': data['a'] + data['b']})