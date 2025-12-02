# HashMap Implementations – Open Addressing & Chaining

**Course:** CS261 - Data Structures  
**Assignment:** Assignment 6  
**Author:** Ken Wheeler  
**Due Date:** 6/6/24  

---

## 📖 Overview
This project contains **two separate HashMap implementations**:

1. **Open Addressing with Quadratic Probing** (`hash_map_open.py`)  
2. **Chaining with Linked Lists** (`hash_map_chaining.py`)  

Both implementations support dynamic resizing, collision handling, and iteration across stored key/value pairs.  
The design follows CS261 specifications and runs in any editor using **Python 3**.

---

## ⚙️ Features

### 🔹 Open Addressing (`hash_map_open.py`)
- **put(key, value):** Insert/update pairs; resizes when load factor ≥ 0.5.  
- **quadratic_probe():** Resolves collisions via quadratic probing.  
- **resize_table(new_capacity):** Resizes to next prime capacity.  
- **table_load():** Returns load factor.  
- **empty_buckets():** Counts empty slots.  
- **get(key):** Retrieves value or `None`.  
- **contains_key(key):** Checks key existence.  
- **remove(key):** Marks slot as tombstone.  
- **get_keys_and_values():** Returns all active pairs.  
- **clear():** Clears table without changing capacity.  
- **Iteration support:** `__iter__()` and `__next__()` skip tombstones.  

---

### 🔹 Chaining (`hash_map_chaining.py`)
- **put(key, value):** Insert/update pairs; resizes when load factor ≥ 1.0.  
- **resize_table(new_capacity):** Doubles capacity, ensures prime, rehashes all pairs.  
- **table_load():** Returns load factor.  
- **empty_buckets():** Counts empty linked lists.  
- **get(key):** Retrieves value or `None`.  
- **contains_key(key):** Checks key existence via linked list search.  
- **remove(key):** Removes node from linked list.  
- **get_keys_and_values():** Returns all pairs in a dynamic array.  
- **clear():** Clears table without changing capacity.  
- **find_mode(array):** Returns `(DynamicArray of mode(s), highest frequency)` in O(N).  

---

## 🛠️ Requirements
- Python 3.x  
- Provided `DynamicArray`, `HashEntry`, and `LinkedList` classes.  
- No external libraries required.  

---

## ▶️ How to Run
1. Clone or download this repository.  
2. Open in your preferred Python 3 editor (VS Code, PyCharm, IDLE).  
3. Run either implementation file:  

```bash
python3 hash_map_open.py
python3 hash_map_chaining.py

Example Usage
from hash_map_open import HashMap as OpenHashMap
from hash_map_chaining import HashMap as ChainingHashMap

# Open Addressing
hm_open = OpenHashMap()
hm_open.put("apple", 10)
print(hm_open.get("apple"))   # Output: 10

# Chaining
hm_chain = ChainingHashMap()
hm_chain.put("banana", 20)
print(hm_chain.contains_key("banana"))  # Output: True

