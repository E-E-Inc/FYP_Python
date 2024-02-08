import requests
import json

def Calories(query):
    #uses API to get calorie information
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'V9yArwyqPfnqYsxWWwRSng==HTX0HgBcu8SqUeph'})
    portionsize = 2


    # Check response status
    if response.status_code == requests.codes.ok:

        # Load response data
        data = json.loads(response.text)

        # Access the first dictionary in the list
        first_item = data[0]  

        # Access the calories item
        calories = first_item.get('calories')

        # Multiplication based on portion size
        overallcalories = calories * portionsize

        # Printing
        print("Calories per item: ", calories)
        print("Overall Calories: ", overallcalories)
        return overallcalories
    else:
        print("Error:", response.status_code, response.text)