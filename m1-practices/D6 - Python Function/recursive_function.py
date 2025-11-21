def count_down(count):
    print(count)
    count -=1  # count = count - 1
    
    if count >=0:
        count_down(count)


count_down(5)