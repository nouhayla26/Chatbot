from enum import Enum

#constants class

class Path(Enum):
    RECOMMENDER_MATRIX_PATH = "data/recipe_ingr_matrix.npz"
    USER_MATRIX_PATH = 'data/user_array.pkl'
    DATASET_RECIPE_PATH = 'data/dataset_recipe.pkl'
    DF_METATATA_PATH = 'data/df_metadata.json'
    INGR_MAP_PATH = 'data/ingr_map.pkl'
    
class Debug(Enum):
    VERBOSE = True
    
class Treshold(Enum):
    COS_SIM_RECIPE = 0.5