# This code is for slicing the phone number to into this format
# (63)-969-142-3437

def phonenumber(number):
    areacode = "("+ 63 + ")"
    first_code = number[1:2] 
    second_code = number[3:7]
    last_code = number[7-10]
    return areacode + "" + first_code +"-"+second_code+"-"+last_code

phonenumber("09691423437")
