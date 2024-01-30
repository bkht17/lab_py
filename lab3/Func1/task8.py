def spy_game(lst):
    correctlist = [0,0,7]
    list_to_check = []

    for x in lst:
        if x == 0 or x == 7:
            list_to_check.append(x)
    
    if list_to_check == correctlist:
        return True
    else: 
       return False
        
      
    
nums = [int(x) for x in input().split()]
print(spy_game(nums))

