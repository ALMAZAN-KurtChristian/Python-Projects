
def addition_table(given_number):
    iterated_number = 1
    sum_total = 1
    
    while iterated_number <= 5:
        sum_total = given_number + iterated_number
        
        if sum_total >20:
            break
        
        print(str(given_number), "+" ,(str(iterated_number)),"=",(str(sum_total)))
        iterated_number += 1
    

addition_table(5)
addition_table(17)
addition_table(30)

# Expected output:
# 5 + 1 = 6
# 5 + 2 = 7
# 5 + 3 = 8
# 5 + 4 = 9
# 5 + 5 = 10
# 17 + 1 = 18
# 17 + 2 = 19
# 17 + 3 = 20
# None