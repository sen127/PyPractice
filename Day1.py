message = "Hello Python World!"
print(message)
message = "Hello Python Crash Course world!"
print(message)
name = "Ada Lovelace"
print(name.upper())
print(name.lower())

first_name = "Eric"
last_name = "lovelace"
full_name = f"{first_name} {last_name}"
print(f"Hello {first_name}, would you like to learn some python today?")
print(full_name.lower())
print(full_name.upper())
print(full_name.title())

first_name = "albert"
last_name = "einstein    "
full_name = f"{first_name} {last_name}"
print(f'{full_name.rstrip().title()} once said, "A person who never made a mistake never tried anything new."')

fruits = ['apple', 'banana', 'papaya', 'blueberry']
fruits.insert(0, 'starberry')
fruits.sort()
for fruit in fruits:
    print(fruit.title())
del fruits[3]
for fruit in fruits:
    print(sorted(fruits))