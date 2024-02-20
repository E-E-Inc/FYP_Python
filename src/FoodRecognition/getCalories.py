import json
import requests

def Calories(query, portion_size):
    #uses API to get calorie information
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'V9yArwyqPfnqYsxWWwRSng==HTX0HgBcu8SqUeph'})
    cals = 0

    # Check response status
    if response.status_code == requests.codes.ok:

        # Load response data
        data = json.loads(response.text)

        # Access the first dictionary in the list
        first_item = data[0]  

        # Access the calories item
        calories = first_item.get('calories')

        if calories is not None:
            # Multiplication based on portion size
            overall_calories = int(calories) * int(portion_size)
            cals = overall_calories
            return overall_calories  
    else:
        print("Error:", response.status_code, response.text)

    return cals
