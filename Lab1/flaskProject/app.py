from flask import Flask, request
import requests
import uuid
app = Flask(__name__)


@app.route('/facade_service', methods=['POST', 'GET'])
def hello_world():  # put application's code here
    if request.method == 'GET':
        to_return_logging =  requests.get('http://127.0.0.1:8081/logging')
        to_return_msgs = requests.get('http://127.0.0.1:8082/messages')

        return '<p>Logging: ' + to_return_logging.content.decode('ascii') + '</p>' +\
               '<p>Msgs:' + to_return_msgs.content.decode('ascii') + '</p>'
    if request.method == 'POST':
        id = uuid.uuid1()
        requests.post('http://127.0.0.1:8081/logging', json={str(id): request.json['msg']})
        return "Message sent"

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
