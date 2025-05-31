
#Simple Format in Codes
def student_grade(name,number):
    return "{} received {} on the exam".format(name, number)

print(student_grade("KURT", 100))
print(student_grade("Christian", 80))

def product_price(Base):
    Taxed = Base * 1.09
    return "Base price of the product is ${:.2f} and with tax is ${:.2f}".format(Base, Taxed)

print(product_price(7.2121))

def format_design(Name, Age):
    return " {:>3} | {:>6.2f}".format(Name, Age)

def format_design(Name, Age):
    return f" {Name:>3} | {float(Age):>6.2f}"

print(format_design("Amy", 21))
print(format_design("Mely", 22))


