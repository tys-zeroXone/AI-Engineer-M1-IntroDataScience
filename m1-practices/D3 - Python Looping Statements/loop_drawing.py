# case 1
print("case 1")
stars = ""

for i in range(5):
    stars += "* " # stars = stars + "* "
print(stars)

# case 2
print("case 2")
stars = ""

for i in range(5):
    stars += "*\n" # stars = stars + "* "
print(stars)

# case 3

stars = ""
size = 5

for i in range(size):
    for j in range(size):
        stars += "*"
    stars+="\n"
print(stars)

# case 4
stars = ""
size = 5
for i in range(size):
    for j in range(1+i):
        stars += "* "
    stars+="\n"
print(stars)