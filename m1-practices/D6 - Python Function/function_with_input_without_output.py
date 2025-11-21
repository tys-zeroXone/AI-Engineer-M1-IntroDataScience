def salam(nama, usia, hobi): # function dengan input # paramater di fungsi ini adalah nama, usia, hobi
    print(f"Halo nama saya {nama} dan usia saya adalah {usia}")
    print("Senang berkenalan dengan anda")
    print("Hobi saya adalah:")
    for x in hobi:
        print("-", x)
    # tanpa output ngga ada return value
    
salam("arif", 21) # argumennya adalah arif, 21, dan list dari hobi

# salam(nama="caca", hobi=["jalan-jalan"], usia=17)