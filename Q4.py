def fibonacci(n):
    # According to the definition: return n if n is 0 or 1; otherwise return the sum of the previous two terms
    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

# Test n = 3, 9, 15
test_cases = [3, 9, 15]
for n in test_cases:
    print(f"F_{n} = {fibonacci(n)}")