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

aliens = []
for alien_number in range(30):
    new_alien = {'color': 'greeen', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)
print(aliens)

prompt = "If you share your name, we can personlaize the messages you see."
prompt = prompt + "\nWhat is your name?\n>"
name = input(prompt)
print(f"\nHello, {name}!")
age = int(input("How old are you, " + name + "?, if you don't mind me asking?\n>"))
if age < 18:
    print("Oh! You're quite young!")
elif age >= 18 and age < 65:
    print("Oh! so you're an adult! " + name + "!")