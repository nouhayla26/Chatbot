import requests
import time

def test():
    url = 'http://127.0.0.1:5000/recommend'
    params = {
        'excluded_ingredients': ['salt', 'sugar'],
        'included_ingredients': ['chicken', 'rice'],
        'number_recipes': 3
    }

    # Capture the start time
    start_time = time.time()

    # Make the request
    response = requests.get(url, params=params)

    # Capture the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the response data and elapsed time
        return response.text, elapsed_time
    else:
        # Handle unsuccessful response
        return f"Error: {response.status_code}", None

if __name__ == "__main__":
    response_text, elapsed_time = test()
    print("Response Text:", response_text)
    print("Elapsed Time:", elapsed_time, "seconds")