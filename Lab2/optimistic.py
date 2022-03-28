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
        while True:
            value = map.get(key)
            newValue = value + 1
            time.sleep(0.01)

            if map.replace_if_same(key, value, newValue):
                break

    print(map.get(key))