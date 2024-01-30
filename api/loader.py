import pickle
import pandas as pd
import numpy as np
from scipy import sparse
import json
from sklearn.feature_extraction.text import CountVectorizer
import ast

#constants class
from constants import *
from utils import print_green


def load_recommendation_matrix(verbose=Debug.VERBOSE.value):
    if verbose:
        print_green('Loading recommendation matrix')

    np_matrix = sparse.load_npz(Path.RECOMMENDER_MATRIX_PATH.value).toarray()
    
    with open(Path.DF_METATATA_PATH.value, 'r') as f:
        df_metadata = json.load(f)
        
    recommendation_matrix = pd.DataFrame(np_matrix, columns=df_metadata['columns'], index=df_metadata['index'])
    
    return recommendation_matrix


def load_user_matrix(verbose=Debug.VERBOSE.value):
    if verbose:
        print_green('Loading user matrix')
    with open(Path.USER_MATRIX_PATH.value, 'rb') as handle:
        user_matrix = pickle.load(handle)
    return user_matrix


def load_dataset_recipe(verbose=Debug.VERBOSE.value):
    if verbose:
        print_green('Loading dataset recipe')
    with open(Path.DATASET_RECIPE_PATH.value, 'rb') as handle:
        user_matrix = pickle.load(handle)
        
    user_matrix['ingredient_ids'] = user_matrix['ingredient_ids'].apply(ast.literal_eval)
    return user_matrix


def save_user_matrix(user_matrix, verbose=Debug.VERBOSE.value):
    if verbose:
        print_green('Saving user matrix')
    with open(Path.USER_MATRIX_PATH.value, 'wb') as handle:
        pickle.dump(user_matrix, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        
def load_ingr_map(verbose=Debug.VERBOSE.value):
    if verbose:
        print_green('Loading ingr map')
    ingr_map = pd.read_pickle(Path.INGR_MAP_PATH.value)
    return ingr_map


def init_ingr_vectorizer(ingr_map, verbose=Debug.VERBOSE.value):
    if verbose:
        print_green('Initializing ingr vectorizer')
    ingr_vectorizer = CountVectorizer()
    ingr_vectorizer.fit(ingr_map['replaced'])
    
    return ingr_vectorizer