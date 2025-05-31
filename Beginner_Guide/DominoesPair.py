
#Code for the two dice scenario 
#Left is the first dice
#Right is the second dice

for left in range(7):
    for right in range(left,7):
        print("[", str(left), "|" ,str(right),"]",sep=" ")
    print()