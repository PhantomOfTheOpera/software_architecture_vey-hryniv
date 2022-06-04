from flask import Flask
import flask
import hazelcast
import consul
import random
import string
import requests

app = Flask(__name__)
all_table = {}
map = None
@app.route('/logging',methods=['POST','GET'])
def hello_world():  # put application's code here
    global all_table,map

    if flask.request.method == 'GET':
        return ' '.join(map.values())
    else:
        key = list(flask.request.json.keys())[0]
        map.lock(key)
        map.put(key, flask.request.json[key])
        map.unlock(key)
        return 'No world'

if __name__ == '__main__':
    hz = hazelcast.HazelcastClient()
    c = consul.Consul()
    host_port = 8081
    host_name = '127.0.0.1'
    host = '127.0.0.1:' + str(host_port)
    service_name = "logging_" + str(host)
    c.agent.service.register(service_name, port=host_port)
    map_name = c.kv.get("hz-map")[1]
    if not map_name:
        generate_map_name = "map-for-flask"     # Тут я генерую ім'я для мапи, якщо воно ще не існує, тому я не міг взнати його за допомогою consul
        map = hz.get_map(generate_map_name).blocking()
        c.kv.put("hz-map",generate_map_name)
    else:
        map_name = map_name['Value'].decode('ascii')
        map = hz.get_map(map_name).blocking()

    app.run(port=host_port,host=host_name)
