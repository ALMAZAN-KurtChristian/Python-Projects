Sorthat = { "Gryffindor" : 0, "Ravenclaw": 0, "Hufflepuff": 0, "Slytherin": 0 }


print("Do you like Dawn or Dusk?")
# print ("1) Dawn")
# print ("2) Dusk")
print ("""
1) Dawn
2) Dusk
""")
Q1=int(input())

if  Q1 == 1:
  Sorthat["Gryffindor"] += 1
  Sorthat["Ravenclaw"] += 1
elif Q1 == 2:
  Sorthat["Hufflepuff"] += 1
  Sorthat["Slytherin"] += 1
else:
  print("Wrong Input")

print (""" 
Q2) When I’m dead, I want people to remember me as:
    1) The Good
    2) The Great
    3) The Wise
    4) The Bold
""")

Q2 = int(input())

if Q2 == 1:
  Sorthat["Hufflepuff"] += 2
elif Q2 == 2:
  Sorthat["Slytherin"] += 2
elif Q2 == 3:
  Sorthat["Ravenclaw"] += 2
elif Q2 == 4:
  Sorthat["Gryffindor"] += 2
else:
  print("Wrong Input")



print(""" 
Q3) Which kind of instrument most pleases your ear?
    1) The violin
    2) The trumpet
    3) The piano
    4) The drum
""")

Q3 = int(input())

if Q3 == 2 :
  Sorthat["Hufflepuff"] += 4
elif Q2 ==1:
  Sorthat["Slytherin"] += 4
elif Q2 == 3:
  Sorthat["Ravenclaw"] += 4
elif Q2 == 4:
  Sorthat["Gryffindor"] += 4
else:
  print("Wrong Input")


highest_house = max(Sorthat, key=Sorthat.get)

# Get the highest value
highest_value = Sorthat[highest_house]

# Print the house with the highest value and its value
print(f"The house with the highest value is {highest_house} with a value of {highest_value}")
  
