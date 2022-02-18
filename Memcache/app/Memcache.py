import random
import sys
from collections import OrderedDict


# https://www.geeksforgeeks.org/lru-cache-in-python-using-ordereddict/
class Memcache:

    def __init__(self, capacity=2, policy="LRU"):
        self.cache = OrderedDict()
        # miss rate information
        self.num_requests = 0  # int
        self.num_miss = 0  # int

        # utilization over time
        self.num_items = 0  # int
        self.size = 0  # Bytes

        # configuration parameters
        self.capacity = capacity  # MB
        self.policy = policy  # "LRU" or "Random"
        # TODO: update settings from database
        self.refresh_config()

    def __str__(self):
        msg = "------ configuration parameters -------\n" \
              + "capacity: {} MB\npolicy: {}\n" \
              + "-------- utilization over time --------\n" \
              + "# of items: {}\ntotal size: {} MB\n" \
              + "-------- miss rate information --------\n" \
              + "# of requests: {}\n# of miss: {}\nmiss rate: {}\nhit rate: {}\n" \
              + "------------- keys stored -------------\n" \
              + str(list(self.cache.keys())) + "\n" \
              + "---------------------------------------"
        if self.num_requests == 0:
            miss_rate = 1
        else:
            miss_rate = self.num_miss / self.num_requests

        return msg.format(self.capacity, self.policy,
                          self.num_items, self.size / 1024 / 1024,
                          self.num_requests, self.num_miss,
                          miss_rate, 1 - miss_rate)

    def get(self, key):
        self.num_requests += 1
        if key not in self.cache:
            self.num_miss += 1
            return -1
        else:
            # LRU policy
            if self.policy == "LRU":
                self.cache.move_to_end(key)  # the LRU item goes to the end of queue
            # random policy
            # do nothing

            return self.cache[key]

    def put(self, key, value):
        element_size = sys.getsizeof(value)
        if element_size > self.capacity * 1024 * 1024:
            return -1
        # if key already exists, remove the item in order to recalculate the cache size
        if key in self.cache:
            self.invalidate_key(key)

        self.free_space(element_size)
        self.num_items += 1
        self.size += element_size
        self.cache[key] = value

        # LRU policy
        if self.policy == "LRU":
            self.cache.move_to_end(key)
        # random policy
        # do nothing
        return 0

    def free_space(self, required_size):
        while self.size + required_size > self.capacity * 1024 * 1024:  # out of capacity
            # LRU policy
            if self.policy == "LRU":
                item = self.cache.popitem(last=False)[1]  # remove the first item
            # random policy
            else:
                item = self.cache.pop(random.choice(list(self.cache.keys())))  # remove a random item
            self.num_items -= 1
            self.size -= sys.getsizeof(item)

    def clear(self):
        self.num_items = 0
        self.size = 0
        self.cache.clear()

    def invalidate_key(self, key):
        if key not in self.cache:
            return -1
        else:
            item = self.cache.pop(key)
            self.num_items -= 1
            self.size -= sys.getsizeof(item)

            return 0

    # read mem-cache related details from the database and reconfigure it based on the values set by the user
    def refresh_config(self):
        # TODO: update settings from database
        pass

    # the current statistics for the mem-cache over the past 10 minutes
    def write_statistics(self):
        # TODO: write statistics into database
        print("Writing statistics into database...")
