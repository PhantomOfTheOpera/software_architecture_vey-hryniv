from flask import Flask
import flask
import hazelcast
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
    map = hz.get_map("map-for-flask").blocking()
    app.run(port=8081)
