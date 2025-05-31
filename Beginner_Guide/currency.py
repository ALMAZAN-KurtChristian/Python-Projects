# Currency Changer

CO = int(input("What do you have left in pesos? "))
PE = int(input("What do you have left in soles? "))
BR = int(input("What do you have left in reais? "))

#Conversion of Currencies to USD - MARCH 3 2025
#0.00024 = 1 $
#0.27 = 1 $
#0.17 = 1 $
Convert =  0.00024 * CO + 0.27 * PE +  .17 * BR

print (Convert)