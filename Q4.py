def fibonacci(n):
    # Base cases: F(0) = 0, F(1) = 1
    if n <= 1:
        return n
    
    # Initialize the first two numbers of the sequence
    a, b = 0, 1
    
    # Iterate from the 2nd to the nth number using a for loop
    for i in range(2, n + 1):
        # Update values: next number is the sum of previous two
        a, b = b, a + b
    return b

# Test cases as required: n = 3, 9, 15
for n in [3, 9, 15]:
    print(f"Fibonacci number F({n}) = {fibonacci(n)}")