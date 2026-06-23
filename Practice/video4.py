# --- 1. Math vs Strings (Your previous code) ---
x = 12345
print(f"Extracting digits mathematically from {x}:")
for i in range(5):
    y = x % 10   # Get the last digit
    x = x // 10  # Chop off the last digit
    print(f"Digit: {y} | Remaining: {x}")

print("\n" + "="*40 + "\n")

# --- 2. Cycle Reduction (Your current question) ---




# The Naive Approach: 
for i in range(11):
    if i % 2 == 0:  # Asking the ALU to do math and check True/False
        print(i)


# The Optimized Approach: Just jump by 2, don't even check!
for i in range(0, 11, 2):  # Start at 0, stop at 10, step by 2
    print(i)
