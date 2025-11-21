numbers = [41, 5, 1, 3, 89, 32]

min_val = numbers[0]
max_val = numbers[0]

for x in numbers:
    if x < min_val:
        min_val = x
    if x > max_val:
        max_val = x
print("Numbers = {}".format(numbers))
print("Min value = {}".format(min_val))
print("Max value= {}".format(max_val))