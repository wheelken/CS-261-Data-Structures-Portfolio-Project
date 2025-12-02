# CS-261-Data-Structures-Portfolio-Project
HashMap Implementation 
# HashMap Implementation (Open Addressing)

**Author:** Ken Wheeler  
**Due Date:** 6/6/24  

---

## Overview
This project implements a **HashMap** using **open addressing with quadratic probing**.  
The implementation supports dynamic resizing, tombstone handling, and iteration across stored key/value pairs.  

The design follows the requirements of CS261 and is intended to run in any editor using **Python 3**.

---

## Features
- **put(key, value):** Insert or update key/value pairs. Resizes table when load factor ≥ 0.5.  
- **quadratic_probe():** Helper for resolving collisions via quadratic probing.  
- **resize_table(new_capacity):** Dynamically resizes the table to the next prime capacity.  
- **table_load():** Returns current load factor.  
- **empty_buckets():** Returns number of empty buckets.  
- **get(key):** Retrieves value for a given key, or `None` if not found.  
- **contains_key(key):** Checks if a key exists in the map.  
- **remove(key):** Removes a key/value pair by marking the slot as a tombstone.  
- **get_keys_and_values():** Returns a dynamic array of all active key/value pairs.  
- **clear():** Clears the table without changing capacity.  
- **Iteration support:** `__iter__()` and `__next__()` allow traversal of active entries.  

---

## Requirements
- Python 3.x  
- No external libraries required (uses provided `DynamicArray` and `HashEntry` classes).  

---

##  How to Run
1. Clone or download this repository.  
2. Open the project in your preferred Python 3 editor (e.g., VS Code, PyCharm, or IDLE).  
3. Run the file containing the `HashMap` class.  
4. Use the provided methods to test functionality. Example:

```python
from hash_map import HashMap

# Create a new hash map
hm = HashMap()

# Insert key/value pairs
hm.put("apple", 10)
hm.put("banana", 20)

# Retrieve values
print(hm.get("apple"))   # Output: 10
print(hm.contains_key("banana"))  # Output: True

# Remove a key
hm.remove("apple")
print(hm.get("apple"))   # Output: None
