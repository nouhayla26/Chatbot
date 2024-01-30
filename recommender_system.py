import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast

#constants class
from constants import Debug
from utils import load_recommendation_matrix, load_user_matrix, load_dataset_recipe, load_ingr_map


def select_best_recipe(recommendation_matrix, user_array, n=50):
    """
    compute the cosine similarity between the user array and the recipe array. retrieve the n best recipes
    Args:
        n (int, optional): Number of recipe to retrieve. Defaults to 1.

    Returns:
        recipe_index array(int): index of the best recipes (shape (1,n))
    """
    cos_sim = cosine_similarity([user_array], recommendation_matrix)
    n_best_indices = np.argsort(cos_sim[0])[-n:]  # Access the first row of cos_sim
    
    return recommendation_matrix.iloc[n_best_indices.tolist()]


def update_vector_weight_2(user_vector, recommendation_matrix, ingr_ids, increase=True):
    #function to update the user vector based on the ingredient ids (weight update = 1/4 of the euclidean distance between then nearest boundary (0 or 1))
    column_ids = [recommendation_matrix.columns.get_loc(col) for col in np.array(ingr_ids, dtype=str)]
    for col_id in column_ids:
        if increase:
            boundary_diff = (1 - user_vector[col_id]) / 4
            user_vector[col_id] = min(1, user_vector[col_id] + boundary_diff)
        else:
            boundary_diff = user_vector[col_id] / 4
            user_vector[col_id] = max(0, user_vector[col_id] - boundary_diff)
    return user_vector



def update_vector_weight(user_vector, recommendation_matrix, ingr_ids, increase=True):
    # Convert ingr_ids to numpy array
    ingr_ids = np.array(ingr_ids, dtype=str)
    
    # Get column indices
    column_ids = recommendation_matrix.columns.get_indexer(ingr_ids)
    
    # Compute boundary_diff
    if increase:
        boundary_diff = (1 - user_vector[column_ids]) / 4
        user_vector[column_ids] = np.minimum(1, user_vector[column_ids] + boundary_diff)
    else:
        boundary_diff = user_vector[column_ids] / 4
        user_vector[column_ids] = np.maximum(0, user_vector[column_ids] - boundary_diff)
    
    return user_vector


       
def filter_recipe(df_recipe, 
                  max_ingredients=None, 
                  max_steps=None, 
                  max_minutes=None, 
                  max_calories=None, 
                  excluded_ingredient_ids=None, 
                  included_ingredient_ids=None, 
                  return_id=True, 
                  verbose=Debug.VERBOSE.value):

    """Function to filter recipe based on provided constraints
    
    Args:
        df_recipe (pd.Dataframe): recipe dataframe
        max_ingredients (int, optional): max ingredient of the recipe. Defaults to None.
        max_steps (int, optional): max step of the recipe. Defaults to None.
        max_minutes (int, optional): max minutes of the recipe. Defaults to None.
        max_calories (int, optional): max calories of the recipe. Defaults to None.
        excluded_ingredient_ids (list(int), optional): list of ingredient id to exclude from the recipe. Defaults to None.
        included_ingredient_ids (list(int), optional): list of ingredient id to include in the recipe. Defaults to None.
        return_id (bool, optional): return list of id if set to true else return dataframe. Defaults to True.
        verbose (bool, optional): debug mode. Defaults to VERBOSE.

    Returns:
        pd.Dataframe: dataframe of filtered recipe (if return_id = False)
        Index(id): list of id of filtered recipe (if return_id = True)
    """
    
    if max_ingredients is not None:
        if verbose:
            print('Filtering recipes with less than {} ingredients'.format(max_ingredients))
        df_recipe = df_recipe[df_recipe['n_ingredients'] <= max_ingredients]
        
    if max_steps is not None:
        if verbose:
            print('Filtering recipes with less than {} steps'.format(max_steps))
        df_recipe = df_recipe[df_recipe['n_steps'] <= max_steps]
        
    if max_calories is not None:
        if verbose:
            print('Filtering recipes with less than {} calories'.format(max_calories))
        df_recipe = df_recipe[df_recipe['calories'] <= max_calories]
        
    if max_minutes is not None:
        if verbose:
            print('Filtering recipes with less than {} minutes'.format(max_minutes))
        df_recipe = df_recipe[df_recipe['minutes'] <= max_minutes]
        
    if excluded_ingredient_ids is not None:
        if verbose:
            print('Filtering recipes excluding ingredients {}'.format(excluded_ingredient_ids))
        df_recipe = df_recipe[~df_recipe['ingredient_ids'].apply(lambda x: any(ingredient in x for ingredient in excluded_ingredient_ids))]
        
    if included_ingredient_ids is not None:
        if verbose:
            print('Filtering recipes including ingredients {}'.format(included_ingredient_ids))
        df_recipe = df_recipe[df_recipe['ingredient_ids'].apply(lambda x: all(ingredient in x for ingredient in included_ingredient_ids))]
            
    if return_id:
        return df_recipe['id']
    else:
        return df_recipe
    

def recommend_best_recipe(user_vector, 
                          df_recipe, 
                          recommendation_matrix, 
                          max_ingredients=None, 
                          max_steps=None, 
                          max_minutes=None, 
                          max_calories=None, 
                          excluded_ingredient_ids=None, 
                          included_ingredient_ids=None, 
                          number_recipes=1, 
                          random_picking=True):
    """
    Function to recommend the best recipe based on the user vector / recommandation matrix based on constraints
    
    Args:
        user_vector (np.array): user vector of shape (1, n_ingredients)
        df_recipe (pd.Dataframe): recipe dataframe
        recommendation_matrix (pd.Dataframe): recommendation matrix of shape (n_recipes, n_ingredients)
        max_ingredients (int, optional): max ingredient of the recipe. Defaults to None.
        max_steps (int, optional): max step of the recipe. Defaults to None.
        max_minutes (int, optional): max minutes of the recipe. Defaults to None.
        max_calories (int, optional): max calories of the recipe. Defaults to None.
        excluded_ingredient_ids (list(int), optional): list of ingredient id to exclude from the recipe. Defaults to None.
        included_ingredient_ids (list(int), optional): list of ingredient id to include in the recipe. Defaults to None.
        number_recipes (int, optional): number of recipe to recommend. Defaults to 1.
        random_picking (bool, optional): random picking between selected recipe 
                                         (avoid to select the same recipe again and again if the user vector don't change). Defaults to True.

    Returns:
        pd.Dataframe: dataframe of the best selected recipe (shape[0] = number_recipes)
    """
    
    #Filter the recipe list based on provided parameters
    df_recipe_filtered = filter_recipe(df_recipe, 
                                       max_ingredients=max_ingredients, 
                                       max_steps=max_steps, 
                                       max_minutes=max_minutes, 
                                       max_calories=max_calories, 
                                       excluded_ingredient_ids=excluded_ingredient_ids, 
                                       included_ingredient_ids=included_ingredient_ids)
    
    
    #Compute the cosine similarity between the user vector and the recipe matrix to select best recipes
    if random_picking and number_recipes > 1:
        # Randomly pick n recipe from the filtered list (n = number_recipes)
        recipes = select_best_recipe(recommendation_matrix.loc[df_recipe_filtered], user_vector)
        #TO REMOVE -> RANDOM STATE FOR TESTING PURPOSE
        recipes = recipes.sample(n=number_recipes, random_state=1)
    else:
        # No random picking, select the best n recipes
        recipes = select_best_recipe(recommendation_matrix.loc[df_recipe_filtered], user_vector, n=number_recipes)

    
    return df_recipe[df_recipe['id'].isin(recipes.index)]
    
    


"""
if __name__ == '__main__':
    
    recommendation_matrix = load_recommendation_matrix()
    user_matrix = load_user_matrix()
    dataset_recipe = load_dataset_recipe()
    
    res = recommend_best_recipe(user_matrix, dataset_recipe, recommendation_matrix, included_ingredient_ids=[1257, 7655, 6270], max_calories=500, number_recipes=5)
    
    print(res['ingredient_ids'].iloc[0])
    print(res.head())
    
    user_matrix = update_vector_weight(user_matrix, recommendation_matrix, [1257, 7655, 6270], increase=True)
    
    print(recommend_best_recipe(user_matrix, dataset_recipe, recommendation_matrix, included_ingredient_ids=[1257, 7655, 6270], max_calories=500, number_recipes=5))
"""
