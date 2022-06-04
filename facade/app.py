import random
from flask import Flask, request
import hazelcast
import requests
import uuid
import consul
import string
import time
app = Flask(__name__)
last_update_time = 0
hosts_logging = []
hosts_messages = []
@app.route('/facade_service', methods=['POST', 'GET'])
def facade():  # put application's code here
    # Get logging port and messages port
    global last_update_time
    global hosts_logging,hosts_messages
    if time.time() - last_update_time > 60: # Last update was more than minute ago
        hosts_logging = []
        hosts_messages = []
        for i in c.agent.services():
            if i.startswith('logging'):
                hosts_logging.append('http://' + i.split('_')[1] + '/logging')
            if i.startswith('messages'):
                hosts_messages.append('http://' + i.split('_')[1] + '/messages')
        last_update_time = time.time()

    get_logging = random.choice(hosts_logging)
    get_msgs = random.choice(hosts_messages)

    if request.method == 'GET':
        to_return_logging = requests.get(get_logging)
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
    c = consul.Consul()
    host_port = 8085
    host_name = '127.0.0.1'
    host = '127.0.0.1:' + str(host_port)
    service_name = "facade_" + str(host)

    c.agent.service.register(service_name, port=host_port)



    # Connect to hz queue
    queue_name = c.kv.get("hz-queue")[1]

    if not queue_name:
        generate_queue_name = "queue-for-flask"     # Тут я генерую ім'я для черги, якщо воно ще не існує, тому я не міг взнати його за допомогою consul
        queue = hz.get_map(generate_queue_name).blocking()
        c.kv.put("hz-queue",generate_queue_name)
    else:
        queue_name = queue_name['Value'].decode('ascii')
        queue = hz.get_queue(queue_name).blocking()


    app.run( port=host_port,host=host_name)
