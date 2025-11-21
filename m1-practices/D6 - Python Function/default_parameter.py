def salam(nama="Unknown", usia=0):
    if nama != "Unknown":
        print(f"Halo nama saya {nama}")
    if usia != 0:
        print(f"Usia saya {usia}")
    else:
        print("Halo semuanya")


salam("arif", 21)
salam("arif")
salam(21)
salam()
       

def luas_lingkaran(phi=3.14, radius=0):
    print(phi, radius)
    luas = phi * radius * radius
    print(luas)

luas_lingkaran()