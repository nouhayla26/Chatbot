from sklearn.metrics.pairwise import cosine_similarity
import re

#constants class
from constants import *

def print_green(message):
    print("\033[92m" + message + "\033[0m")


def print_red(message):
    print("\033[91m" + message + "\033[0m")
    
    
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip()

    return text
        
        
def map_recipe_id2str(ingr_map, recipe_id):
    # Filter DataFrame for matching recipe_id
    filtered = ingr_map[ingr_map['id'] == recipe_id]
    
    if filtered.empty:
        return None
    #return maching string if id is found
    return filtered['replaced'].values[0]


def map_recipe_str2id(ingr_vectorizer, ingr_map, input_strs, threshold=Treshold.COS_SIM_RECIPE.value, verbose=Debug.VERBOSE.value):
    
    ingredient_ids = []
    gpt_res_msg = ""
    for input_str in input_strs:
        input_str = preprocess_text(input_str)
        # Transform the input string
        X = ingr_vectorizer.transform([input_str])
        
        # Calculate cosine similarity between input string and food strings
        similarities = cosine_similarity(X, ingr_vectorizer.transform(ingr_map['replaced']))[0]
        
        # Find the index of the food string with the highest similarity
        max_similarity_index = similarities.argmax()
        if verbose:
            print("[map_recipe_str2id] input: ", input_str)
            
        # Check if the similarity is above the threshold
        if similarities[max_similarity_index] >= threshold:
            # Return the corresponding food IDvectorizer
            closest_food_id = ingr_map.iloc[max_similarity_index]['id']
            if verbose:
                print_green(f"[map_recipe_str2id] Found : {ingr_map.iloc[max_similarity_index]['replaced']} percent: {similarities[max_similarity_index]}")
            ingredient_ids.append(closest_food_id)
        else:
            # No food name is close enough
            if verbose:
                print_red("map_recipe_str2id] No matching recipe found")
            gpt_res_msg += f"Ingredient {input_str} not found in our database. "
    return ingredient_ids, gpt_res_msg

"""
if __name__ == "__main__":
    ingr_map = load_ingr_map()
    
    ingr_vectorizer = init_ingr_vectorizer(ingr_map)
    print(map_recipe_str2id(ingr_vectorizer, ["boloss", "chicken", "rice", "salt", "sugar", "pepper", "tomato"]))
"""