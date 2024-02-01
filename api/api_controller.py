
from flask import Flask, request, jsonify, render_template
from utils import *
from loader import *
from recommender_system import recommend_best_recipe, update_vector_weight
import logging
import time
import chainlit as cl
import threading
import subprocess

app = Flask(__name__, static_folder=Path.STATIC_FOLDER_PATH.value, template_folder=Path.TEMPLATE_FOLDER_PATH.value)

recommendation_matrix = load_recommendation_matrix()
df_recipe = load_dataset_recipe()
ingr_map = load_ingr_map()
ingr_vectorizer = init_ingr_vectorizer(ingr_map)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)


def get_param(name, convert_func=int):
    value = request.args.get(name)
    return convert_func(value) if value is not None else None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=['GET'])
def recommend():
    start_time = time.time()
    
    max_ingredients = get_param('max_ingredients')
    max_steps = get_param('max_steps')
    max_minutes = get_param('max_minutes')
    max_calories = get_param('max_calories')
    number_recipes = get_param('number_recipes') or 1

    excluded_ingredients = request.args.getlist('excluded_ingredients') or []
    included_ingredients = request.args.getlist('included_ingredients') or []
    
    print("Max Ingredients:", max_ingredients)
    print("Max Steps:", max_steps)
    print("Max Minutes:", max_minutes)
    print("Max Calories:", max_calories)
    print("Excluded Ingredients:", excluded_ingredients)
    print("Included Ingredients:", included_ingredients)
    print("Number of Recipes:", number_recipes)
    
    print_red(f"Extracting parameters time: {time.time() - start_time}")

    excluded_ingredient_ids, gpt_res_msg = map_recipe_str2id(ingr_vectorizer, ingr_map, excluded_ingredients)
    print_red(f"Extracting ingredient ID1 time:: {time.time() - start_time}")
    included_ingredient_ids, gpt_res_msg_incl = map_recipe_str2id(ingr_vectorizer, ingr_map, included_ingredients)
    gpt_res_msg += gpt_res_msg_incl
    
    
    print_red(f"Extracting ingredient IDs time:: {time.time() - start_time}")
    
    user_matrix = load_user_matrix()
    recommended_recipes = recommend_best_recipe(user_matrix, 
                                               df_recipe, 
                                               recommendation_matrix, 
                                               max_ingredients, 
                                               max_steps, 
                                               max_minutes, 
                                               max_calories, 
                                               excluded_ingredient_ids, 
                                               included_ingredient_ids, 
                                               number_recipes)
    
    print_red(f"Loading user matrix and recommending recipes time: {time.time() - start_time}")
    
    #res_ui = res_chatbot = recommended_recipes[['name', 'minutes', 'n_steps', 'ingredients', 'n_ingredients', 'calories', 'steps']]
    
    res_chatbot = recommended_recipes[['name', 'minutes', 'n_steps', 'ingredients', 'n_ingredients', 'calories']].to_json(orient='records')
    print_green(res_chatbot)
    #TO DO
    #res_rachbot in json params
    res_chatbot += gpt_res_msg 
    
    
    #------------------TO DO UPDATE RECIPE UI------------------
    #update_recipe_UI(recommended_recipes)
    #res_UI = recommended_recipes[['name', 'minutes', 'n_steps', 'ingredients', 'n_ingredients', 'calories', 'steps']].to_json(orient='records') 
    
    return res_chatbot
    

@app.route("/update_user_weight", methods=['POST'])
def update_user_weight_api():
    
    start_time = time.time()
    data = request.get_json()
    increase_weight = data.get('increase_weight')
    ingr_ids = data.get('ingr_str', [])  # Get 'ingr_str' from JSON body
    
    print_red(f"Update user weight: {increase_weight} {ingr_ids}")
    
    if ingr_ids and increase_weight:
        user_matrix = load_user_matrix()
        ingr_ids = map_recipe_str2id(ingr_vectorizer, ingr_map, ingr_ids)[0]
        user_matrix = update_vector_weight(user_matrix, recommendation_matrix, ingr_ids, increase=increase_weight)
        save_user_matrix(user_matrix)
        print_green(f"Update user weight time: {time.time() - start_time}")
        return jsonify({'status': 'success'})
    else:
        print_red(f"User matrix not updated")
        return jsonify({'status': 'error'})


if __name__ == '__main__':
    app.run(debug=True)
    
    