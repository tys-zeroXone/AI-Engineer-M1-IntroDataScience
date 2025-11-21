numbers = [41, 5, 1, 3, 89, 32]

print('List Sebelum Di Sort = {}'.format(numbers))

for i in range(len(numbers) - 1) :
    for j in range(i+1,len(numbers)) :
        if(numbers[i] > numbers[j]) :
            numbers[i],numbers[j] = numbers[j],numbers[i]
        
print('List Setelah Di Sort = {}'.format(numbers))