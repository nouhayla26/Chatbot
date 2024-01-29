import pickle
import pandas as pd
import numpy as np
from scipy import sparse
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

#constants class
from constants import *


def load_recommendation_matrix(verbose=Debug.VERBOSE.value):
    if verbose:
        print('Loading recommendation matrix')

    np_matrix = sparse.load_npz("recipe_ingr_matrix.npz").toarray()
    
    with open(Path.DF_METATATA_PATH.value, 'r') as f:
        df_metadata = json.load(f)
        
    recommendation_matrix = pd.DataFrame(np_matrix, columns=df_metadata['columns'], index=df_metadata['index'])
    
    return recommendation_matrix


def load_user_matrix(verbose=Debug.VERBOSE.value):
    if verbose:
        print('Loading user matrix')
    with open(Path.USER_MATRIX_PATH.value, 'rb') as handle:
        user_matrix = pickle.load(handle)
    return user_matrix


def load_dataset_recipe(verbose=Debug.VERBOSE.value):
    if verbose:
        print('Loading dataset recipe')
    with open(Path.DATASET_RECIPE_PATH.value, 'rb') as handle:
        user_matrix = pickle.load(handle)
    return user_matrix


def save_user_matrix(user_matrix, verbose=Debug.VERBOSE.value):
    if verbose:
        print('Saving user matrix')
    with open(Path.USER_MATRIX_PATH.value, 'wb') as handle:
        pickle.dump(user_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        
def load_ingr_map(verbose=Debug.VERBOSE.value):
    if verbose:
        print('Loading ingr map')
    ingr_map = pd.read_pickle(Path.INGR_MAP_PATH.value)
    return ingr_map


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
    

def map_recipe_str2id(ingr_map, input_str, threshold=Treshold.COS_SIM_RECIPE.value, verbose=Debug.VERBOSE.value):
    
    input_str = preprocess_text(input_str)
    # Fit and transform the input string and food strings
    vectorizer = CountVectorizer()
    corpus = [input_str] + list(ingr_map['replaced'])
    X = vectorizer.fit_transform(corpus)
    
    # Calculate cosine similarity between input string and food strings
    similarities = cosine_similarity(X)[0][1:]
    
    # Find the index of the food string with the highest similarity
    max_similarity_index = similarities.argmax()
    if verbose:
        print("[map_recipe_str2id] input: ", input_str)
        
    # Check if the similarity is above the threshold
    if similarities[max_similarity_index] >= threshold:
        # Return the corresponding food ID
        closest_food_id = ingr_map.iloc[max_similarity_index]['id']
        if verbose:
            print_green(f"map_recipe_str2id] Found : {ingr_map.iloc[max_similarity_index]['replaced']} percent: {similarities[max_similarity_index]}")
        return closest_food_id
    else:
        # No food name is close enough
        if verbose:
            print_red("map_recipe_str2id] No matching recipe found")
        return None


if __name__ == "__main__":
    ingr_map = load_ingr_map()
    print(map_recipe_str2id(ingr_map, "chicken"))
    