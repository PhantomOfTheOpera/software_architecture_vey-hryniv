from flask import Flask,request
import hazelcast
import consul
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

    c = consul.Consul()

    hz = hazelcast.HazelcastClient()
    host_port = 8087
    host_name = '127.0.0.1'
    host = '127.0.0.1:' + str(host_port)
    service_name = "messages_" + str(host)

    c.agent.service.register(service_name, port=host_port)


    queue_name = c.kv.get("hz-queue")[1]
    if not queue_name:
        generate_queue_name = "queue-for-flask"     # Тут я генерую ім'я для черги, якщо воно ще не існує, тому я не міг взнати його за допомогою consul
        queue = hz.get_map(generate_queue_name).blocking()
        c.kv.put("hz-queue",generate_queue_name)
    else:
        queue_name = queue_name['Value'].decode('ascii')
        queue = hz.get_queue(queue_name).blocking()


    app.run(port=host_port,host=host_name)
