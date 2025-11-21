z = range(10)
for x in z:
    print(x, end=" ")
    if x == 5:
        break
    

z = range(3, 100, 7)
search = 45
for x in z:
    print(x)
    if x == search:
        print("Data ditemukan")
        break
    