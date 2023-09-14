# HashTable Class
# Adapted from code used in 'How to Dijkstra' Webinar

class HashTable:
    # Initializes the hash map with size as input,
    # if no input provided the default will be 40 based on initial pacakge count
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert function will add the item into the hash table with the key and value
    # If key doesn't exist it will be added, if the key exists the value will be updated
    # Space-time complexity is O(1)
    def insert(self, key, item):  # Provides insert and update functionality
        # Get hash value to determine bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update key if it already exists in bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If key is not present, it is added to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # The look_up function searches the hash table for the provided key and returns the value
    # Space-time complexity is O(1)
    def look_up(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]


        # search for the key in the bucket list
        for kv in bucket_list:

            if kv[0] == key:
                return kv[1]  # value
        return None

    # Function to print all items in the hash table
    # Space-time complexity is O(N) for N items in table
    def print_all(self):
        for item in self.table:
            if len(item) != 0:
                print(item[0][1].package_id, item[0][1].address, item[0][1].city, item[0][1].state,
                      item[0][1].zip, item[0][1].deadline, item[0][1].mass, item[0][1].status)
