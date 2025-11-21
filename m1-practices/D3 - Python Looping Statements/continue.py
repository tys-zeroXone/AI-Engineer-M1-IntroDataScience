z = range(5)

for x in z:
    print(x)
    
print("-----")

for x in z:
    if x == 3:
        continue
    print(x)
    print("selamat datang di toko kami")