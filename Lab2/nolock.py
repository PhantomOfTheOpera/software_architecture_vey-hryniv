import time

import hazelcast

if __name__ == "__main__":
    # Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
    hz = hazelcast.HazelcastClient()
    key = "1"
    map = hz.get_map("my-distributed-map").blocking()
    map.put(key, 0)

    for i in range(1000):
        if i % 100 == 0:
            print("AT:", i)
        time.sleep(0.01)
        value = map.get(key)
        value += 1
        map.put(key, value)
    print(map.get(key))