import openai
import json
from chatbot_functions import recipes_list, ingredients_list, find_recipes_by_ingredients, find_recipes_by_name

# openai.api_key = openai_api_key

"""Content of the initial message prompt, describing the role and tasks of 
a cook who consults the recipes, the associated ingredients, the preparation 
time and the different stages thereof., along with menu items and restrictions."""
messages = [{
    "role": "system", 
    "content": "A cook. Take a recipe name, give the associated ingredients, the preparation time and the different stages of it. Only offer a description of recipes from the following list, no inventions beyond this list of recipes :" 
    + ', '.join(recipes_list) +
    """\nCan also take one or more ingredients and give the recipe name that contains these ingredients or similar ingredients, the ingredients associated to the recipe, the preparation time and different stages of it. The ingredients list for all recipes is as follows. No inventions beyond this ingredient list: """ 
    + ', '.join(ingredients_list) +
    """ . Respond naturally and with relevant and funny emojii always."""
            }]
#print(messages)




def get_answer(question):
    question = str(question) + "\n Response 500 chars maximum: generate short reply. No non-food Qs allowed."
    messages.append({'role': 'user', 'content': question})
    functions = [
    {
        "name": "find_recipes_by_ingredients",
        "description": """Retrieve the name of a recipe and its various informations such as its ingredients, the time required for its preparation, its different steps. Perfect function for searching recipes in a database against the name of a specific recipe.""",
        "parameters": {
            "type": "object",
            "properties": {
                "df_recipes": {
                    "type": "object",
                    "description": "Pandas DataFrame that contains all recipes data.",
                },
                "query": {
                    "type": "string",
                    "description": "One or more ingredients given by the user.",
                },
            },
            "required": [ "query"],
        },
    },
    {
        "name": "find_recipes_by_name",
        "description": """Retrieve the name of a recipe and its various information such as its ingredients, the time required for its preparation, its different steps from ingredients given by the user. Perfect function for searching and recommending recipes based on one or more user-specified ingredients.""",
        "parameters": {
            "type": "object",
            "properties": {
                "df_recipes": {
                    "type": "object",
                    "description": "Pandas DataFrame that contains all recipes data.",
                },
                "query": {
                    "type": "string",
                    "description": "Name of recipe given by the user.",
                },
            },
            "required": ["query"],
        },
    },
    # We can Add other functions as needed here !!!
]
    
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto",  
        )
    response_message = response["choices"][0]["message"]


    if response_message.get("function_call"):

        available_functions = {
            'find_recipes_by_ingredients': find_recipes_by_ingredients,
            "find_recipes_by_name": find_recipes_by_name,
        }

        function_name = response_message["function_call"]["name"]
        print(function_name)

        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)

        function_response = fuction_to_call(function_args)
        print(function_response)


        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": str(function_response),
            }
        )


        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            temperature=0,
            #max_tokens=256,
        )  # get a new response from GPT where it can see the function response

        messages.append({"role": "assistant", "content": second_response["choices"][0]["message"]["content"]})
        print(second_response["usage"])

        return second_response["choices"][0]["message"]["content"]
    else:
        messages.append({"role": "assistant", "content": response_message["content"]})
        print(response["usage"])
        print(messages)
        return response_message["content"]       










if __name__ == '__main__':
    print(get_answer("How much is pizza margherita?"))
    #print(type(beer_list))
    
