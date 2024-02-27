import json
import requests

def getNutrientInfo(query, portion_size):
    #uses API to get calorie information
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'V9yArwyqPfnqYsxWWwRSng==HTX0HgBcu8SqUeph'})
        
    # list to store nutrients 
    nutrients = []
   
    # Check response status
    if response.status_code == requests.codes.ok:

        # Load response data
        data = json.loads(response.text)
                    
        # Check if the data contains nutrient information
        if isinstance(data, list) and len(data) > 0:
            food_data = data[0]
            # Construct a nutrient dictionary and multiply by portion size
            nutrient = {
                'name': food_data.get('name'),
                'calories per 100g': food_data.get('calories') * portion_size,
                'serving_size_g': food_data.get('serving_size_g')  * portion_size,
                'fat_total_g': food_data.get('fat_total_g')  * portion_size,
                'fat_saturated_g': food_data.get('fat_saturated_g')  * portion_size,
                'protein_g': food_data.get('protein_g')  * portion_size,
                'sodium_mg': food_data.get('sodium_mg')  * portion_size,
                'potassium_mg': food_data.get('potassium_mg')  * portion_size,
                'cholesterol_mg': food_data.get('cholesterol_mg')  * portion_size,
                'carbohydrates_total_g': food_data.get('carbohydrates_total_g')  * portion_size,
                'fiber_g': food_data.get('fiber_g')  * portion_size,
                'sugar_g': food_data.get('sugar_g')  * portion_size
            }
            nutrients.append(nutrient)
            print(nutrients)
        else:
            print("Nutrient data not found in the API response")
    else:
        print("Error:", response.status_code, response.text)

    return data

# query = "Banana"
# portion_size = 1
# getNutrientInfo(query, portion_size)