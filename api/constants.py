from enum import Enum
import os

#constants class

class Path(Enum):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    RECOMMENDER_MATRIX_PATH = os.path.join(BASE_DIR, "data/recipe_ingr_matrix.npz")
    USER_MATRIX_PATH = os.path.join(BASE_DIR, 'data/user_array.pkl')
    DATASET_RECIPE_PATH = os.path.join(BASE_DIR, 'data/dataset_recipe.pkl')
    DF_METATATA_PATH = os.path.join(BASE_DIR, 'data/df_metadata.json')
    INGR_MAP_PATH = os.path.join(BASE_DIR, 'data/ingr_map.pkl')
    STATIC_FOLDER_PATH = os.path.join(BASE_DIR, 'template/static')
    TEMPLATE_FOLDER_PATH = os.path.join(BASE_DIR, 'template')
    CHATBOT_PROCESS_PATH = os.path.join(BASE_DIR, "api/chatbot_process.py")
    API_PROCESS_PATH = os.path.join(BASE_DIR, "api/api_controller.py")
    
class Debug(Enum):
    VERBOSE = True
    
class Treshold(Enum):
    COS_SIM_RECIPE = 0.5