import time

import hazelcast

if __name__ == "__main__":
    hz = hazelcast.HazelcastClient()
    queue = hz.get_queue("queue").blocking()
    print("Capacity:", queue.remaining_capacity())
    for i in range(20):
        queue.put(i)
        print(queue.remaining_capacity())
