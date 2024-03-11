import json
import requests

def BMR(gender, age, height, weight):
    total = 0

    # if gender is woman 
    if(gender=="female"):
        total = 655.1 + (9.563 *  float(weight)) + (1.85 * float(height)) - (4.676 * int(age))
        return total
    
    # if gender is male
    if(gender=="male"):
        total = 66.47 + (13.75 *  float(weight)) + (5.003 * float(height)) - (6.755 * int(age))
        return total

    return total
