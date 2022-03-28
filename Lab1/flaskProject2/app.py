from flask import Flask
import flask
import requests
app = Flask(__name__)
all_table = {}

@app.route('/logging',methods=['POST','GET'])
def hello_world():  # put application's code here
    global all_table
    if flask.request.method == 'GET':
        return ' '.join(all_table.values())
    else:
        key = list(flask.request.json.keys())[0]
        all_table[key] = flask.request.json[key]
        print(all_table)
        return 'No world'

if __name__ == '__main__':
    app.run(port=8081)
