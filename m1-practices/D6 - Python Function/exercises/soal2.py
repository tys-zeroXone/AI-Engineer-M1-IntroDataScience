def filter_gaji(listGaji) :
    return list(filter(lambda gaji : gaji * 95/100 > 9000000, listGaji))

list1 = [9100000,9800000,9500000,10300000,9300000]

list1 = filter_gaji(list1)

print(list1)