import random

from flask import Flask, request
import hazelcast
import requests
import uuid
app = Flask(__name__)
hosts = ['http://127.0.0.1:8081/logging','http://127.0.0.1:8082/logging','http://127.0.0.1:8083/logging']
hosts_messages = ['http://127.0.0.1:8084/messages','http://127.0.0.1:8086/messages']
@app.route('/facade_service', methods=['POST', 'GET'])
def hello_world():  # put application's code here
    get_logging = random.choice(hosts)
    get_msgs = random.choice(hosts_messages)
    print(get_logging)
    print(get_msgs)
    if request.method == 'GET':
        to_return_logging =  requests.get(get_logging)
        to_return_msgs = requests.get(get_msgs)

        return '<p>Logging: ' + to_return_logging.content.decode('ascii') + '</p>' +\
               '<p>Msgs:' + to_return_msgs.content.decode('ascii') + '</p>'
    if request.method == 'POST':
        queue.add(request.json['msg'])
        requests.post(get_msgs)
        id = uuid.uuid1()
        requests.post(get_logging, json={str(id): request.json['msg']})
        return "Message sent"

if __name__ == '__main__':
    hz = hazelcast.HazelcastClient()
    queue = hz.get_queue("queue-for-flask").blocking()
    app.run( port=8085)
