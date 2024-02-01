import requests
import time

def test_recommender():
    url = 'http://127.0.0.1:5000/recommend'
    params = {
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
    

def test_update_user_weight():
    url = 'http://127.0.0.1:5000/update_user_weight'
    data = {
        'increase_weight': True,
        'ingr_str': ['chicken', 'rice']
    }

    # Capture the start time
    start_time = time.time()

    # Make the request
    response = requests.post(url, json=data)

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
    response_text, elapsed_time = test_recommender()
    print("Response Text recommander:", response_text)
    print("Elapsed Time recommander:", elapsed_time, "seconds")
    response_text_weight, elapsed_time_weight = test_update_user_weight()
    print("Response Text weight:", response_text_weight)
    print("Elapsed Time weight:", elapsed_time_weight, "seconds")