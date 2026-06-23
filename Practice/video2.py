# x = f"The total is {2*5:10f}"
# print(x)

# BANKER'S ROUNDING
# x =6
# print("Even"*(x%2==0) or  "Odd"*(x%2!=0))

# WALRUS OPERATOR (:=)
# Problem 2.1: Use the Walrus Operator to simplify input loops.
# The Walrus operator assigns a value to a variable AND returns it at the same time.
# This avoids having to write 'val = input()' twice (once before and once inside the loop).




# while (val := input("Enter a positive number or 'stop': ")) != 'stop':
#     print(f"You entered {val}")





# val = input("Enter a positive number or 'stop': ") # taking a input 
# while val != 'stop':                                  # checking a condition 
#     print(f"You entered {val}")
#     val = input("Enter a positive number or 'stop': ") # taking a input again 




"""
Question 1:
Problem 2.2: Deep Short-Circuit Logic
Without running the code, dictate exactly what each variable will hold and why based on the python runtime stack.
"""

# SOLUTIONS:


val1 = 0 and "Python"            # val1 = 0
# REASON: 'and' returns the FIRST falsy value it hits. 0 is falsy, so it stops immediately.

val2 = "Apple" or "Banana"       # val2 = "Apple"
# REASON: 'or' returns the FIRST truthy value it hits. "Apple" is truthy, so it stops immediately.

val3 = "" or [] or 10             # val3 = 10
# REASON: 'or' skips falsy values like "" and []. 10 is the first truthy value it finds.

val4 = 6 and True and "Code"      # val4 = "Code"


# REASON: 'and' checks everything looking for a falsy value. Since all (6, True) are truthy, 
# it returns the very LAST value evaluated.



# FIZZBUZZ (NO IF STATEMENTS)
# Problem 2.3: Mathematical Boolean Logic
# Task: Ask for N, output Fizz, Buzz, FizzBuzz or N.

# TRICK: 
# 1. "Fizz" * True (1)  -> "Fizz"
# 2. "Fizz" * False (0) -> ""
# 3. Use 'or' to return N if the result of concatenation is an empty string.

N = int(input("Enter an integer N: "))

result = ("Fizz" * (N % 3 == 0) + "Buzz" * (N % 5 == 0)) or N

print(f"For {N=}, Result: {result}")