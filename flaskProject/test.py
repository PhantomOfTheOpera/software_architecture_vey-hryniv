import requests
for i in range(10):
    requests.post('http://127.0.0.1:8085/facade_service', json={f'msg': f'msg-{i}'})
