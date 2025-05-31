import random

Question = input("Question: ")
num = random.randint (1,9)

if num == 1:
  print ("Magic 8 Ball: Yes - definitely.")
elif num ==2 :
  print("Magic 8 Ball: It is decidedly so.")
elif num ==3 :
  print("Magic 8 Ball: Without a doubt.")
elif num ==4 :
  print("Magic 8 Ball: Reply hazy, try again.")
elif num ==5 :
  print("Magic 8 Ball: Ask again later.")
elif num ==6 :
  print("Magic 8 Ball: Better not tell you now.")
elif num ==7 :
  print("Magic 8 Ball: My sources say no.")
elif num ==8 :
  print("Magic 8 Ball: Outlook not so good.")
else:
  print ("Magic 8 Ball: Very doubtful.")


