# Advanced Python: Real-World Closures and Decorators

This document moves beyond the theory to show you exactly *why* and *how* professional engineers use **Closures** and **Decorators** in production code. 

---

## 1. Real-World Closures 

A closure exists when an inner function remembers the state of its outer function, even after the outer function has finished running. We use closures to **hide data** (privatization) and to create **function factories**.

### Example 1: Data Hiding & State (The "Bank Account" Pattern)
In languages like Java or C++, you have `private` variables that prevent users from accidentally changing a value directly (like forcing `balance` to 0). Python does not have strict private variables. Instead, we can use a closure!

```python
def create_bank_account(initial_balance):
    # This variable is "hidden" inside the closure. 
    # Nobody outside this function can ever touch it directly!
    balance = initial_balance 
    
    def transaction(amount):
        # We must tell Python we are modifying the outer scoped variable
        nonlocal balance  
        balance += amount
        return balance

    # We return the inner function pointer, not the result
    return transaction

# Create an account
my_account = create_bank_account(100)

print(my_account(50))   # Deposits 50 -> Output: 150
print(my_account(-20))  # Withdraws 20 -> Output: 130

# TRICK: There is absolutely no way to do `my_account.balance = 1000000`. 
# The variable is physically shielded inside the closure's memory snapshot!
```

### Example 2: The "Configuration Factory"
When building web scrapers or APIs, you often need to fetch data from the same URL base but different endpoints. Instead of typing the base URL everywhere, you can use a closure to "bake in" the configuration.

```python
def api_fetcher_factory(base_url):
    # The inner function permanently remembers the base_url
    def fetch_endpoint(endpoint):
        full_url = f"{base_url}/{endpoint}"
        print(f"Fetching data from: {full_url}")
        # In real code: return requests.get(full_url)
        return {"status": 200, "data": "Success"}
    
    return fetch_endpoint

# Bake in the configurations once
github_api = api_fetcher_factory("https://api.github.com/v3")
twitter_api = api_fetcher_factory("https://api.twitter.com/v2")

# Now we have beautifully clean function calls!
github_api("users/choclate/repos")
twitter_api("tweets/12345")
```

---

## 2. Real-World Decorators

Decorators allow you to permanently graft new behavior onto existing functions without modifying their source code. They rely heavily on closures.

### Target Scenario: The Flaky Internet (Automatic Retries)
Imagine writing a script that scrapes a website or connects to an unreliable MySQL database. Sometimes, the connection randomly drops. You don't want your whole app to crash on the first failure.

Instead of writing `try/except` loops inside *every single database function*, you write **one** decorator.

```python
import time
import random

def retry_on_failure(func):
    """A decorator that automatically retries a flaky function up to 3 times."""
    
    def wrapper(*args, **kwargs):
        attempts = 3
        while attempts > 0:
            try:
                # Attempt to execute the original function
                result = func(*args, **kwargs)
                return result  # If it works, instantly return
                
            except Exception as e:
                attempts -= 1
                print(f"[{func.__name__}] Failed! Retrying... ({attempts} attempts left)")
                time.sleep(1) # Wait 1 second before retrying
                
        # If it fails 3 times, let it crash.
        print("Function completely failed after 3 retries.")
        raise Exception("Fatal Error.")
        
    return wrapper

# -- USAGE -- 

@retry_on_failure
def unstable_database_call():
    # Simulate a flaky connection (70% chance to crash)
    if random.random() < 0.70:
        raise ConnectionError("Server disconnected suddenly!")
    return "Database data retrieved successfully!"


# If you run this, you will see the decorator automatically catching errors 
# and re-running the function for you behind the scenes!
print(unstable_database_call())
```

### Target Scenario: Caching / Memoization (Making slow code 1000x faster)
If you have a function that does heavy math or reaches out to a slow API, and you foresee calling it multiple times with the exact same inputs, you can attach a "Cache" decorator. 

```python
def cache_results(func):
    # This dictionary acts as our closure state! 
    # It lives forever in the decorator's backpack.
    memory = {}
    
    def wrapper(*args):
        # We use the function arguments as the dictionary key
        if args in memory:
            print(f"Retrieving cached result for {args}...")
            return memory[args]
            
        # If it's a new input, let the function do the heavy lifting
        print(f"Calculating heavy computation for {args}...")
        result = func(*args)
        
        # Save it into the backpack for next time!
        memory[args] = result
        return result
        
    return wrapper

@cache_results
def heavy_math(x, y):
    time.sleep(2)  # Simulate 2 seconds of heavy processing
    return x * y

# First time: Takes 2 seconds to run
print(heavy_math(10, 5)) 

# Second time: Instant! The decorator intercepts it and hands back the saved answer.
print(heavy_math(10, 5)) 
```

---

## 3. Advanced Pro-Tricks 

### Trick 1: `functools.wraps` (Don't lose your identity!)
There is a massive hidden danger when using decorators. When you put `@my_decorator` on top of your `def calculate():` function, Python actively *replaces* your function with the decorator's `wrapper` function. 

If someone types `print(calculate.__name__)` or tries to read your docstrings later in the code, Python will literally print `wrapper` instead of `calculate`! You lose all debugging metadata.

**The Fix:** Professional developers ALWAYS use `from functools import wraps`.

```python
from functools import wraps

def proper_decorator(func):
    # This magic line commands the wrapper to steal the name, 
    # identity, and docstrings of original 'func'
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Doing something before...")
        return func(*args, **kwargs)
        
    return wrapper

@proper_decorator
def login():
    """Logs the user into the server."""
    pass

# Because we used @wraps, this safely prints 'login' instead of 'wrapper'!
print(login.__name__)
```

### Trick 2: Decorator Stacking
You can apply multiple decorators to a single function. They execute from **bottom to top** (closest to the function first).

```python
@retry_on_failure  # Runs second (wraps the cached wrapper)
@cache_results     # Runs first (wraps the target function)
def fetch_user_data(user_id):
    # Reaches out to the internet
    pass
```
This single function now has bullet-proof networking AND blazing speed, completely cleanly, without adding a single line of logic inside the function itself!
