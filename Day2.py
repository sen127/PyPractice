car = 'subaru'
print("Is car == 'subaru'? I predict True.")
print(car == 'subaru')

print("\nIs car == 'audi'? I predict False.")
print(car == 'audi')

squares = []
for value in range(1,11):
    squares.append(value**2)
print(squares)
print(min(squares[0:4]))
print(max(squares))
print(sum(squares))
value = str(input("Enter a number to search in squares: "))
if value in squares:
    print(f"Found {value} in squares")
else:
    print(f"{value} not found in squares")