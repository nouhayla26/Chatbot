import requests
import time


# Function for recommender system 
def recipes_recommender(**kwargs):
    url = 'http://127.0.0.1:5000/recommend'
    response = requests.get(url, params=kwargs)

    if response.status_code == 200:
    # Return the response data and elapsed time
        return response.text
    else:
    # Handle unsuccessful response
        return f"Error: {response.status_code}", None


