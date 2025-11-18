import random
class random_num_gen:
    def __init__(self, range_max):
        self.range_max = range_max

    def generate_random_numbers(self):
        random_integer_1 = random.randint(1, self.range_max)
        random_integer_2 = random.randint(1, self.range_max)
        return random_integer_1, random_integer_2   

range_max = int(input("Press enter the max limit of the range: "))
rng = random_num_gen(range_max)
print(f"First random number is {random_integer_1}, and second random number is {random_integer_2} and the product of both is {random_integer_1 * random_integer_2}")