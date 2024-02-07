import requests
from testing import s

#uses API to get calorie information
query = s
api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
response = requests.get(api_url, headers={'X-Api-Key': 'V9yArwyqPfnqYsxWWwRSng==HTX0HgBcu8SqUeph'})

# Check response status
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)
