import requests
from IdentifyFood import s

#uses API to get calorie information
api_key = 'qqHgtz06WvIxKvqX0pw40y0B59RLtmcuAVLopwO0'

base_url = 'https://api.nal.usda.gov/fdc/v1/'

food_name = s

# Create session to make api requests
session = requests.Session()
session.params = {'api_key': api_key}

# Searches for food item
search_url = base_url + 'foods/search'

# Make API request
response = session.get(search_url, params={'query': food_name})

# if there is a 200 response then its good!
if response.status_code == 200:

    # Preprocesses the response data
    data = response.json()

    # Check if the key "Foods" exists in database
    if data['foods']:
        # Access first result
        fdc_id = data['foods'][0]['fdcId']

        # Get nutritional information for food item
        nutrient_url = base_url + f'food/{fdc_id}'
        nutrient_response = session.get(nutrient_url)

        if nutrient_response.status_code == 200:
            nutrient_data = nutrient_response.json()

            if 'foodNutrients' in nutrient_data:
                # Print Name and FDC ID
                print(f"Food Name: {nutrient_data['description']}")
                print(f"FDC ID: {nutrient_data['fdcId']}")

                # Print nutrient information
                for nutrient in nutrient_data['foodNutrients']:
                    nutrient_name = nutrient['nutrient']['name']
                    nutrient_value = nutrient['amount']
                    nutrient_unit = nutrient['nutrient']['unitName']
                    print(f"{nutrient_name}: {nutrient_value} {nutrient_unit}")

            else:
                print(f"Nutrient information not found for {food_name}")
        else:
            print(f"Error retrieving nutritional information")
    else:
        print(f"{food_name} not found in the database")
else:
    print(f"Error in the search request")
