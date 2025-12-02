# Name: Ken Wheeler
# OSU Email: wheelken@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - HashMapImplementation Open Addressing
# Due Date: 6/6/24
# Descriptions:
#
# put() - Updates the key/value pair in the hash table. If the current load factor of the table is >= 0.5, the table is
# resized to double its current capacity. If the key already exists in the table, its value is replaced with the
# parameter value. First the load factor is checked and resize is called as needed. The index is calculated and
# if it is empty (None) or a tombstone, a HashEntry is created with the key/value pair. If the index's HashEntry has
# a matching key, the value is replaced. Otherwise, the method probes for the next available index by calling
# _quadratic_probe(). The new_index is returned; a HashEntry is created with the key/value pair or the current
# value at the index is replaced (depending on conditions). If  a new HashEntry is created, size is incremented and
# if a value is replaced size is not incremented.
#
# quadratic_probe() - Helper method for quadratic probing. It receives an index that will serve as the starting point
# for quadratic probing, and the key that will also act as a condition to stop probing. This method returns the new
# index after probing. The method uses 3 conditions stop probing in a while loop: if the new_index is None, if
# is_tombstone is True for the index, or if the parameter key matches the index's key.
#
# resize_table() - Changes the capacity of the underlying table with all active key/value (non-tombstone) pairs placed
# into the new table. First new_capacity is checked to ensure it's not less than the current size. If it is the
# method exits. If new_capacity is valid, its value is checked to ensure it's a prime number.  If the value is not
# prime, next_prime() is called to replace it with the next highest prime number. A new DynamicArray object is
# initialized with None values as placeholders; these will be replaced as needed when put() is called to rehash the
# values. The current hash table is stored in prev_buckets, the current underlying DynamicArray is replaced by the
# new array, capacity is updated to new_capacity, and size is set 0. The size is updated in put() as values are
# rehashed.
#
# table_load()- Returns the current hash table load factor - size/capacity.
#
# empty_buckets() - returns the number of empty buckets in the hash table: self._capacity - self._size
#
# get() - Returns the value associated with the given key; if the key is not in the hash
# map, the method returns None. The index of the key is calculated and if not empty, its value equals the key, and
# is_tombstone is False, the current value is replaced. If none of those conditions are True, the method calls
# # _quadratic_probe() to find the new_index. Those same conditions are then tested with the new_index value.
#
# contains_key() - Returns True if the given key is in the hash map, otherwise it returns False. The first condition
# checked for is an empty table (self._size) == 0. If that condition is True, False is returned. Otherwise, the index
# of the key is calculated and if not empty, its value equals the key, and is_tombstone is False, True is returned.
# If none of those conditions are True, the method calls _quadratic_probe() to find the new_index. The same tests
# are repeated on the new_index. If the correct HashEntry is found True is returned; False is returned otherwise.
#
# remove() - Removes the given key and its associated value from the hash table. The initial index is calculated and
# if the index is not empty and matches the key, it becomes a tombstone and size is decremented. Otherwise, the method
# uses quadratic probing and repeats the same tests until the appropriate index is found. In this case the index also
# becomes a tombstone and size is decremented.
#
# def get_keys_and_values() - Returns a dynamic array with each index containing a tuple of each key/value pair stored
# in the hash table. This method works by creating a new DynamicArray object then traversing the hash table. It then
# creates a tuple of each active key/value pair, and calls append() from the DynamicArray class to add them. The new
# array is then returned.
#
# clear() - Clears the contents of the hash map without altering the capacity. The method works by traversing the
# underlying DynamicArray and setting each index to None. It ends by setting size to 0.
#
# __iter__() - This method enables the hash map to iterate across itself. Its design is mirrored from instructor
# provided code in Module 3. It works by returning the next available item in the underlying DynamicArray.
#
# __next__() - This method will return the next item in the hash table based on the current location of the
# iterator. The design is inspired by instructor provided code in Module 3. The iterator skips over None
# HashEntry's and those with is_tombstone set to True.
#
# Grader notes: I was unable to refactor remove() to use my helper method for quadratic probing. I'm sure its something
# simple, but I'm exhausted and out of time. I would greatly appreciate your feedback.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    def put(self, key: str, value: object, resizing=False) -> None:
        """
        Updates the key/value pair in the hash table; if the current load factor of the table is >= 0.5, the table is
        resized to double its current capacity

        param - key - if the key already exists in the hash table, its value is replaced with the parameter value

        param - value - the corresponding value to the parameter key

        returns - no return value with key/value pair added, or the previous value replaced if the key was already
        present
        """

        # if the current load factor of the table is >=0.5 resize to double its capacity.
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        # determine the index
        index = self._hash_function(key) % self._capacity

        # if the index is  empty or a tombstone, it's available
        if (self._buckets[index] is None) or (self._buckets[index].is_tombstone is True):
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
            return

        # if it's a duplicate update the value and don't update size
        if self._buckets[index].key == key:
            self._buckets[index].value = value
            return

        # quadratic probing
        new_index = self._quadratic_probe(index, key)
        if (self._buckets[new_index] is None) or (self._buckets[new_index].is_tombstone is True):
            self._buckets[new_index] = HashEntry(key, value)
            self._size += 1
            return

            # check for a duplicate
        if self._buckets[new_index].key == key:
            self._buckets[new_index].value = value
            return

    def _quadratic_probe(self, curr_index: int, key) -> int:
        """
        Helper method for quadratic probing
        param - curr_index - the starting point for quadratic probing
        key - the key that will also act as a condition to stop probing
        return - returns the new_index after probing
        """
        j = 1
        # ensure j does not go beyond the length of available buckets
        while j < self._capacity:

            new_index = (curr_index + j ** 2) % self._capacity

            # if the index is empty or a tombstone, it's available
            if self._buckets[new_index] is None:
                return new_index

            if self._buckets[new_index].is_tombstone is True:
                return new_index

            if self._buckets[new_index].key == key:
                return new_index
            j += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table with all active key/value (non-tombstone) pairs placed
        into the new table

        param - new_capacity- twice the size of the previous capacity; this calculation is handled in put before
        resize_table() is called

        return - no return value, with the hash table doubled in size and active elements rehashed
        """

        # check that new_capacity is not less than the current number of elements in the hash map
        if new_capacity < self._size:
            return

        # If new_capacity is valid, make sure it is a prime number; if not, change it to the next highest prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # new_arr will replace the current DynamicArray
        new_arr = DynamicArray()
        for index in range(new_capacity):
            new_arr.append(None)

        # save the old array  before rehashing
        prev_buckets = self._buckets
        self._buckets = new_arr
        self._capacity = new_capacity

        # size is updated in put
        self._size = 0

        for index in range(prev_buckets.length()):
            if prev_buckets[index] is not None:
                # put method will handle the insertion
                self.put(prev_buckets[index].key, prev_buckets[index].value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        param - no parameters

        return - return the table load factor (self._size/self._capacity)
        """

        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        param - no parameters

        return - returns the number of empty buckets (self._capacity - self._size)
        """

        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key; if the key is not in the hash
        map, the method returns None

        param - key - the corresponding key to value being requested

        return - returns the value of the parameter key if present or None if otherwise
        """

        index = self._hash_function(key) % self._capacity
        if ((self._buckets[index] is not None) and (self._buckets[index].key == key) and
                (self._buckets[index].is_tombstone is False)):
            return self._buckets[index].value

        new_index = self._quadratic_probe(index, key)
        if ((self._buckets[new_index] is not None) and (self._buckets[new_index].key == key) and
                        (self._buckets[new_index].is_tombstone is False)):
            return self._buckets[new_index].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.

        param - key - the corresponding key/value pair whose presence is being tested

        return - returns True if the key is present or False if otherwise
        """

        # empty hash map
        if self._size == 0:
            return False

        index = self._hash_function(key) % self._capacity
        if ((self._buckets[index] is not None) and (self._buckets[index].key == key) and
                self._buckets[index].is_tombstone is False):
            return True

        # probe for the new index and test the same conditions
        new_index = self._quadratic_probe(index, key)

        if ((self._buckets[new_index] is not None) and (self._buckets[new_index].key == key) and
                self._buckets[new_index].is_tombstone is False):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.

        param - key - the corresponding key of the key/value pair to be removed

        return - No return with the key/value pair corresponding to the parameter key being removed (if present)
        """

        index = self._hash_function(key) % self._capacity

        # if the index is not empty and matches the key
        if ((self._buckets[index] is not None) and (self._buckets[index].key == key) and
                self._buckets[index].is_tombstone is False):
            self._buckets[index].is_tombstone = True
            self._size -= 1
            return

        # probe for the bucket matching the key
        j = 1
        while j < self._capacity:
            new_index = (index + j ** 2) % self._capacity
            if self._buckets[new_index] is None:
                return
            if (self._buckets[new_index].key == key) and (self._buckets[new_index].is_tombstone is False):
                self._buckets[new_index].is_tombstone = True
                self._size -= 1
                return
            j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash table

        param - No parameters

        return - returns a DynamicArray object with each index containing a tuple of each key/value pair
        """

        # traverse the hash table adding the active key/value pairs to new_arr
        new_arr = DynamicArray()
        for hash_entry in self:
            new_tuple = hash_entry.key, hash_entry.value
            new_arr.append(new_tuple)
        return new_arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map

        param - no parameters

        returns - no return value with the contents of the hash map cleared and the capacity unaltered
        """

        # traverse the DynamicArray and set active key/value pairs to None
        for index in range (self._buckets.length()):
            self._buckets[index] = None

        # reset size to 0
        self._size = 0

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself. Mirrored from instructor provided code in Module 3.

        returns the next available item in the underlying DynamicArray
        """
        self._index = 0
        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, based on the current location of the
        iterator. Mirrored from instructor provided code in Module 3.

        The iterator skips over None HashEntry's and those with tombstone indicators set to True
        """
        while self._index < self._capacity:
            hash_entry = self._buckets[self._index]
            self._index += 1
            # pass over empty and tombstone values
            if (hash_entry is not None) and (hash_entry.is_tombstone is not True):
                return hash_entry
        raise StopIteration

