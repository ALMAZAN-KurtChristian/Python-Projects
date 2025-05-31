#Factoring Numbers
def count_factors(given_number):
    factor = 1
    count = 1
    # This "if" block will run if the "given_number" equals 0.
    if given_number == 0:
        return 0
    while factor < given_number:
        if given_number % factor == 0:
            count += 1
        factor += 1
    return count


print(count_factors(0)) # Count value should be 0
print(count_factors(3)) # Should count 2 factors (1x3)
print(count_factors(10)) # Should count 4 factors (1x10, 2x5)
print(count_factors(24)) # Should count 8 factors (1x24, 2x12, 3x8, and 4x6). 