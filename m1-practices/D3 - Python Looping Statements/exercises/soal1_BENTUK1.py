stars = ''
size = 5

for i in range(size) :
    for j in range(size - i) :
        stars += '* '
    stars += '\n'

for i in range(1, size) :
    for j in range(i + 1) :
        stars += '* '
    stars += '\n'

print(stars)