import json
import requests

def BMR(gender, age, height, weight):
    total = 0

    # if gender is woman 
    if(gender=="female"):
        print("female")
        total = 655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
        print(total)
        return total

    # if gender is male
    if(gender=="male"):
        print("male")
        total = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
        return total
    print(total)
    return total

# gender = "female"
# age = 19
# height = 160
# weight = 79

# test = BMR(gender, age, height, weight)
# print("tester", test)