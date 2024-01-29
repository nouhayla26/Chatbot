
from flask import Flask, request, jsonify

from utils import *
from recommender_system import recommend_best_recipe
import requests
import logging
import time

app = Flask(__name__)

recommendation_matrix = load_recommendation_matrix()
df_recipe = load_dataset_recipe()
ingr_map = load_ingr_map()

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/recommend", methods=['GET'])
def recommend():
    start_time = time.time()
    
    max_ingredients = request.args.get('max_ingredients')
    max_ingredients = int(max_ingredients) if max_ingredients is not None else None

    max_steps = request.args.get('max_steps')
    max_steps = int(max_steps) if max_steps is not None else None

    max_minutes = request.args.get('max_minutes')
    max_minutes = int(max_minutes) if max_minutes is not None else None

    max_calories = request.args.get('max_calories')
    max_calories = int(max_calories) if max_calories is not None else None

    excluded_ingredients = request.args.getlist('excluded_ingredients') or None
    included_ingredients = request.args.getlist('included_ingredients') or None

    number_recipes = request.args.get('number_recipes', default=1)
    number_recipes = int(number_recipes)

    print("Max Ingredients:", max_ingredients)
    print("Max Steps:", max_steps)
    print("Max Minutes:", max_minutes)
    print("Max Calories:", max_calories)
    print("Excluded Ingredients:", excluded_ingredients)
    print("Included Ingredients:", included_ingredients)
    print("Number of Recipes:", number_recipes)
    
    print_green("Request received")
    
    print("Extracting parameters time:", time.time() - start_time)

    
    gpt_res_msg = ""
    excluded_ingredient_ids = None
    included_ingredient_ids = None
    
    if excluded_ingredients:
        excluded_ingredient_ids = []
        for ingr in excluded_ingredients:
            ingr_id = map_recipe_str2id(ingr_map, ingr)
            if ingr_id:
                if Debug.VERBOSE.value:
                    print_green("Ingredient {} found in our database".format(ingr))
                excluded_ingredient_ids.append(ingr_id)
            else:
                if Debug.VERBOSE.value:
                    print_red("Ingredient {} not found in our database".format(ingr))
                gpt_res_msg += "Ingredient {} not found in our database. ".format(ingr)
            
    if included_ingredients:
        included_ingredient_ids = []
        for ingr in included_ingredients:
            ingr_id = map_recipe_str2id(ingr_map, ingr)
            if ingr_id:
                if Debug.VERBOSE.value:
                    print_green("Ingredient {} found in our database".format(ingr))
                included_ingredient_ids.append(ingr_id)
            else:
                if Debug.VERBOSE.value:
                    print_red("Ingredient {} not found in our database".format(ingr))
                gpt_res_msg += "Ingredient {} not found in our database. ".format(ingr)
    
    print("Extracting ingredient IDs time:", time.time() - start_time)
    
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
    
    print("Loading user matrix and recommending recipes time:", time.time() - start_time)
    
    res_chatbot = recommended_recipes[['name', 'minutes', 'n_steps', 'ingredients', 'n_ingredients', 'calories']].to_json(orient='records')
    
    res_chatbot += gpt_res_msg  
    #------------------TO DO UPDATE RECIPE UI------------------
    #update_recipe_UI(recommended_recipes)
    #res_UI = recommended_recipes[['name', 'minutes', 'n_steps', 'ingredients', 'n_ingredients', 'calories', 'steps']].to_json(orient='records') 
    
    return res_chatbot
    

@app.route("/update_user_weight", methods=['POST'])
def update_user_weight(increase_weight=True):
    #ADD ingredient list conversion
    user_matrix = load_user_matrix()
    user_matrix = update_user_weight(user_matrix, request.json['recipe_id'], request.json['weight'])
    save_user_matrix(user_matrix)
    return jsonify({'status': 'success'})



def test():
    with app.test_client() as client:
        # Send a POST request to the /recommend route
        url = '/recommend'
        data = {
            'excluded_ingredients': ['salt', 'sugar'],
            'included_ingredients': ['chicken', 'rice'],
            'number_recipes': 3
        }
        print("post")
        response = client.post(url, json=data)

        # Return the response data
        return response.data.decode('utf-8')  # Decode bytes to string if needed
    
if __name__ == '__main__':
    app.run(debug=True)
    print(test())