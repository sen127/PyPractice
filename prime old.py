# Count prime numbers up to n (basic version)
import time

n = int(input("Enter a number: "))

start = time.time()  # start timer

count = 0
for num in range(2, n + 1):
    is_prime = True
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        count += 1

end = time.time()  # end timer

print(f"\nTotal prime numbers up to {n}: {count}")
print(f"Elapsed time: {end - start:.6f} seconds")