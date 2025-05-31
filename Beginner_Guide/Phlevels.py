#Simple PH LEVEL

phlevels = int (input("Enter PH Level: "))

if phlevels > 7:
  print ("Basic")
elif phlevels <7:
  print ("Acidic")
else:
  print("Neutral")