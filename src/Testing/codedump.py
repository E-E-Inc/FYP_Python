 # Check if the data contains nutrient information
        if isinstance(data, list) and len(data) > 0:
            food_data = data[0]  # Extract the first item (assuming it contains nutrient information)
            
            # Construct a nutrient dictionary
            nutrient = {
                'name': food_data.get('name'),
                'calories per 100g': food_data.get('calories'),
                'serving_size_g': food_data.get('serving_size_g'),
                'fat_total_g': food_data.get('fat_total_g'),
                'fat_saturated_g': food_data.get('fat_saturated_g'),
                'protein_g': food_data.get('protein_g'),
                'sodium_mg': food_data.get('sodium_mg'),
                'potassium_mg': food_data.get('potassium_mg'),
                'cholesterol_mg': food_data.get('cholesterol_mg'),
                'carbohydrates_total_g': food_data.get('carbohydrates_total_g'),
                'fiber_g': food_data.get('fiber_g'),
                'sugar_g': food_data.get('sugar_g')
            }
            nutrients.append(nutrient)
            print(nutrients)
        else:
            print("Nutrient data not found in the API response")