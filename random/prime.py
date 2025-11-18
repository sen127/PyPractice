# Count prime numbers up to n (optimized version using previous primes)
import time

n = int(input("Enter a number: "))

start = time.time()

primes = []

for num in range(2, n + 1):
    is_prime = True
    for p in primes:
        if p * p > num:
            break
        if num % p == 0:
            is_prime = False
            break
    if is_prime:
        primes.append(num)

end = time.time()

print(f"\nTotal prime numbers up to {n}: {len(primes)}")
print(f"Elapsed time: {end - start:.6f} seconds")