from flask import Flask

app = Flask(__name__)


@app.route('/messages',methods=['GET'])
def hello_world():  # put application's code here
    return 'Not implemented yet'


if __name__ == '__main__':
    app.run(port=8082)
