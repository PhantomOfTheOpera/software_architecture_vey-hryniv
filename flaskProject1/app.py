from flask import Flask,request
import hazelcast
app = Flask(__name__)

total_data = []
@app.route('/messages',methods=['GET','POST'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        data = None
        while not data:
            data = queue.poll()
        total_data.append(data)
        return "Message received"
    if request.method == 'GET':
        return ' '.join(total_data)

if __name__ == '__main__':
    hz = hazelcast.HazelcastClient()
    queue = hz.get_queue("queue-for-flask").blocking()
    app.run(port=8086)
