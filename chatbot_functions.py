import pandas as pd 
import numpy as np
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# We import data 
df_recipes = pd.read_csv('/Users/nathanwandji/Downloads/recipes_test_data.csv')



# Function to obtain list of recipes 
def recipes_list_function(df):
    # Extract recipes name from column 'name'
    recipe_names = df['name'].tolist()
    #We delete doublons 
    distinct_recipe_names = list(set(recipe_names))
    return distinct_recipe_names

# List of recipes 
recipes_list = recipes_list_function(df_recipes)



# Function to obtain list of ingredients 
def ingredients_list_function(df):
    # Extract all ingredients name from column 'ingredients'
    all_ingredients = df['ingredients'].tolist()
    # We delete doublons
    distinct_ingredients = list(set(all_ingredients))
    return distinct_ingredients

# List of ingredients 
ingredients_list = ingredients_list_function(df_recipes)







# We define our two function to find recipes in our dataframe 

def find_recipes_by_ingredients(df_recipes, query):
    """ 
    Description: 
        Function to find recipes based on one or more ingredients given by the user  
    Args: 
        -df: pandas Dataframe that contains all recipes data
        -query :one or more ingredients given by the user
    Return: 
        -recipe_name: the most similar recipe name that corresponds to the user query 
        -recipe_ingredients : the ingredients of the most similar recipe that corresponds to the user query 
        -recipe_steps : the steps of the most similar recipe that corresponds to the user query
        -recipe_time : the time of the most similar recipe that corresponds to the user query
    """
    # Create a TFIDF Vectorizer
    vectorizer = TfidfVectorizer()
    # Use the vectorizer's fit_transform function
    X = vectorizer.fit_transform(df_recipes['ingredients'])   
    query_vec = vectorizer.transform([query]) 

    # We compute similarity cosinus between query vector and ingredients vector 
    cosine_similarities = cosine_similarity(query_vec, X)

    # Calculate the cosine similarity and sorting the results by descending order
    similarity_list = cosine_similarities[0]
    sorted_indices = similarity_list.argsort()[::-1]

    # We get the 2 most similar list of ingredients with the search query 
    most_similar_recipe_index = sorted_indices[0]
    recipe_name = df_recipes.iloc[most_similar_recipe_index]['name']
    recipe_ingredients = df_recipes.iloc[most_similar_recipe_index]['ingredients']
    recipe_steps =  df_recipes.iloc[most_similar_recipe_index]['steps']
    recipe_time  =  df_recipes.iloc[most_similar_recipe_index]['minutes']

    return recipe_name, recipe_ingredients, recipe_steps, recipe_time
    

def find_recipes_by_name(df_recipes, query):
    """ 
    Description: 
        Function to find recipes based on a name of recipe given by the user 
    Args: 
        -df: Dataframe pandas that contains all recipes data
        -query : name of recipe given by the user
    Return: 
        -recipe_name: the most similar recipe name that corresponds to the user query 
        -recipe_ingredients : the ingredients of the most similar recipe that corresponds to the user query 
        -recipe_steps : the steps of the most similar recipe that corresponds to the user query
        -recipe_time : the time of the most similar recipe that corresponds to the user query
    """
    # Create a TFIDF Vectorizer
    vectorizer = TfidfVectorizer()
    # Use the vectorizer's fit_transform function
    X = vectorizer.fit_transform(df_recipes['name'])   
    query_vec = vectorizer.transform([query])   

    # We compute similarity cosinus between query vector and ingredients vector 
    cosine_similarities = cosine_similarity(query_vec, X)

    # Calculate the cosine similarity and sorting the results by descending order
    similarity_list = cosine_similarities[0]
    sorted_indices = similarity_list.argsort()[::-1]

    # We get the 2 most similar list of ingredients with the search query 
    most_similar_recipe_index = sorted_indices[0]
    recipe_name = df_recipes.iloc[most_similar_recipe_index]['name']
    recipe_ingredients = df_recipes.iloc[most_similar_recipe_index]['ingredients']
    recipe_steps =  df_recipes.iloc[most_similar_recipe_index]['steps']
    recipe_time  =  df_recipes.iloc[most_similar_recipe_index]['minutes']
    
    return recipe_name, recipe_ingredients, recipe_steps, recipe_time
    
