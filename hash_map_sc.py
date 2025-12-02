# Name: Ken Wheeler
# OSU Email: wheelken@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMapImplementation Chaining
# Due Date: 6/6/24
# Descriptions:
#
# put()- Updates the key/value pair in the hash table. If the load factor is >= 1.0, the capacity is doubled. If the
# key is already present, the current value is replaced. If the key is not in the hash map, its added as a new key/value
# pair. The method works by checking the table load and calling resize if its >= 1.0. The index for the key/value pair
# is calculated then contains() from the LinkedList implementation is called. If the node is not None, the current value
# is overwritten. If the node is indeed None this means the key is not present; insert() from the Linked List class is
# called, the key/value pair added, and size incremented.
#
# resize_table() - Doubles the capacity of the underlying table with all existing key/value pairs preserved. The
# new_capacity calculation is handled when called by put(). If the new capacity is less than 1, the method exits. The
# new capacity is checked to ensure it's a prime number. If it's not, next_prime is called to update it. A new
# DynamicArray of the same length as new_capacity is created. It is then updated with empty LinkedList objects. The
# current underlying DynamicArray is copied, then set to reference the new_arr of empty LL objects. The hash table's
# capacity is then set to the new_capacity. This will ensure hash values are recalculated correctly. The size of the
# hash table is set to 0; it will be updated by put() as each key/value pair is rehashed. The previous array is then
# traversed with each non-empty  bucket's data used to call put().
#
# table_load()- Returns the current hash table load factor (size/capacity).
#
# empty_buckets() - Returns the number of empty buckets in the hash table. This method uses a counter variable (total)
# which starts at 0. The underlying DynamicArray is the traversed; total is incremented for each bucket whose LinkedList
# has a length of 0. The total is then returned.
#
# def get(): Returns the value associated with the given key. If the key is not in the hash table, the method returns
# None. The index is calculated; if the node at the index is empty or the key is not present, the method exits.
# Otherwise, the value is extracted and returned.
#
# contains_key() - Returns True if the given key is in the hash table, otherwise it returns False. Since an
# empty hash table does not contain any keys, if the size is 0 False is immediately returned. The index is then
# calculated. If the length() of the LinkedList at the index is greater than zero, and it contains the key, True is
# returned. If neither condition is met, False is returned.
#
# remove() - Removes the given key and its associated value from the hash table. If the key is not present, the
# method exits without an exception being raised. Remove() then calculates the index; if the length of the LinkedList
# at the index is 0 or the key is not present, the method exits. Otherwise, remove() from the LinkedList class is
# called to remove the node containing the key; size is then decremented.
#
# get_keys_and_values() -> Returns a dynamic array where each index contains a tuple of a key/value pair stored in the
# hash table. A new DynamicArray object is created. The underlying DynamicArray is traversed skipping empty buckets
# (Linked List length is 0). When a bucket with key/value pairs is found, a tuple is created from each key/value pair
# and added to the new array. The new array is then returned.
#
# clear() - Clears the contents of the hash map without changing the hash table capacity. The underlying DynamicArray
# is traversed and each index is set to an empty LinkedList. The size of the hash table is then set to 0.
#
# find_mode() - Receives a DynamicArray and returns a tuple containing a DynamicArray containing the mode value(s) of
# the given array and the highest frequency for the mode value(s). This function is implemented with O(N) time
# complexity. It begins by creating a hash table and traversing the parameter array. The strings from the parameter
# array are used as keys and their frequency is used as the corresponding value. If the key is already present, its
# frequency is updated. If the key is not present, put() is called to add it with a frequency of 1. A new DynamicArray
# is created, and get_keys_and_values() is called to replace the previous parameter array. The modified array is
# traversed and the highest_frequency is updated whenever a larger value is found. The new_array is also reset whenever
# this condition is met. If a key with an equal frequency is found, it's added to the new array. The new array (new_arr)
# and highest frequency are then returned.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash table; if the load factor is >= 1.0 the capacity is doubled.

        param - key - the key corresponding to a value to be added. If the key is already present, the current value
        is replaced; if the key is not in the hash table, its added as a new key/value pair

        param - value - the value corresponding to the parameter key

        return - No return value with the hash table updated with the new key/value pair or the previous value replaced
        """

        # if the current load factor of the table >=1.0 the current capacity is doubled
        if self.table_load() >= 1.0:
            self.resize_table(2 * self._capacity)

        index = self._hash_function(key) % self._capacity
        node = self._buckets[index].contains(key)

        # check for duplicates - replace the existing value if the keys match
        if node is not None:
            node.value = value
        else:
            # if the key is not present, add the value and increment size
            self._buckets[index].insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Doubles the capacity of the underlying table with all existing key/value pairs still present

        param - new_capacity - the new_capacity is double the previous capacity; this calculation is handled when called
        by put(), and if it's not a prime number its updated to the next prime number

        return - no return value with the hash table links rehashed and the capacity doubled
        """

        if new_capacity < 1:
            return

        # check for a prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # create a new_arr with the new_capacity
        new_arr = DynamicArray()
        for index in range(new_capacity):
            new_arr.append(LinkedList())

        # save the data for rehashing
        prev_buckets = self._buckets
        self._buckets = new_arr
        self._capacity = new_capacity

        # size is adjusted in put
        self._size = 0

        for index in range(prev_buckets.length()):
            if prev_buckets[index].length() > 0:
                for node in prev_buckets[index]:
                    self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor

        param - no parameters

        return - returns the hash table load factor (size/capacity)
        """

        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        param - no parameters

        return - returns the number of empty buckets in the hash table
        """

        total = 0
        for index in range(self._buckets.length()):
            # the bucket is empty if the length of the LL is 0
            if self._buckets[index].length() == 0:
                total += 1
        return total

    def get(self, key: str):
        """
        Returns the value associated with the given key; if the key is not present None is returned

        param - the key for the element whose value is being requested

        return - the value associated with the given key.
        """

        index = self._hash_function(key) % self._capacity
        node = self._buckets[index].contains(key)
        # if the node is empty or the key is not present at the index, return None
        if (self._buckets[index].length() == 0) or (node is None):
            return

        # if the node is present, extract the value
        return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash table and False if otherwise

        param - the key to search for in the hash table

        return - returns True if the parameter key is present and false if otherwise
        """

        # empty hash table
        if self._size == 0:
            return False

        # check for the key and return False if not present
        index = self._hash_function(key) % self._capacity

        # if the bucket is empty or the key is not in the LL
        if (self._buckets[index].length() > 0) and (self._buckets[index].contains(key) is not None):
            return True

        # return False otherwise
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method exits without an exception being raised.

        param - the key to be removed from the hash table

        return - No return value with the key/value pair being removed if present
        """

        # calculate the index
        index = self._hash_function(key) % self._capacity

        # exit if the bucket is empty or the key is not present
        if (self._buckets[index].length() == 0) or (self._buckets[index].contains(key) is None):
            return

        # remove from the LL and decrement size
        self._buckets[index].remove(key)
        self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map

        param - no parameters

        returns - a DynamicArray containing tuples of each key/value pair in the hash map
        """

        # traverse the hash map then each LL; if it is not empty the key/value pairs are added to the new array
        new_arr = DynamicArray()
        for index in range(self._buckets.length()):
            if self._buckets[index].length() > 0:
                for node in self._buckets[index]:
                    new_tuple = (node.key, node.value)
                    new_arr.append(new_tuple)

        return new_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map.It does not change the underlying hash
        table capacity.

        param - no parameters

        returns - the hash table is set to an empty state, the size is set to 0, and the capacity is not changed.
        """

        # update each bucket to an empty LL
        for index in range(self._buckets.length()):
            self._buckets[index] = LinkedList()

        # update the size of the hash map but not the capacity
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a dynamic array and returns a tuple containing a dynamic array comprising the mode
    value(s) of the given array and the highest frequency for the mode value(s) (implemented with
    O(N) time complexity)

    param - da - a DynamicArray object composed of strings

    returns - returns a tuple with the requested values
    """
    map = HashMap()

    # add each string to the DynamicArray counting the frequencies
    for index in range(da.length()):
        hash_entry = da[index]
        if map.contains_key(hash_entry):
            # if the key is present, add to its count
            frequency = map.get(hash_entry)
            map.put(hash_entry, frequency + 1)
        else:
            # if the key is not present the value is 1
            map.put(hash_entry, 1)

    # start searching for the highest frequency at 0
    highest_frequency = 0
    new_arr = DynamicArray()
    da = map.get_keys_and_values()

    # search for the highest frequency
    for index in range(da.length()):
        # unpack the key and its frequency
        key, frequency = da[index]
        if frequency > highest_frequency:
            # reset new_arr whenever a higher frequency is found and add the key
            highest_frequency = frequency
            new_arr = DynamicArray()
            new_arr.append(key)

        elif frequency == highest_frequency:
            # if another key has the same frequency add it to new_arr
            new_arr.append(key)

    return new_arr, highest_frequency
