def filter_prime(*list):
    newlist = []
    for i in range(len(list)):
        count = 0
        for j in range(1, list[i]+1):
            if(list[i] % j == 0):
                count = count + 1
        
        if(count == 2):
            newlist.append(list[i])
    
    print(newlist)



input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            