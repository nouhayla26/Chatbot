from enum import Enum

#constants class

class Path(Enum):
    RECOMMENDER_MATRIX_PATH = "recipe_ingr_matrix.npz"
    USER_MATRIX_PATH = 'user_array.pkl'
    DATASET_RECIPE_PATH = 'dataset_recipe.pkl'
    DF_METATATA_PATH = 'df_metadata.json'
    INGR_MAP_PATH = 'ingr_map.pkl'
    
class Debug(Enum):
    VERBOSE = True
    
class Treshold(Enum):
    COS_SIM_RECIPE = 0.5