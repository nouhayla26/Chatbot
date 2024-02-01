from openai import OpenAI

client = OpenAI(api_key="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")
import json
from chatbot_functions import recipes_recommender

# Configuration de la clé API OpenAI
"""Content of the initial message prompt, describing the role and tasks of 
a cook who consults the recipes, the associated ingredients, the preparation 
time and the different stages thereof., along with menu items and restrictions."""
messages = [{
   "role": "system",
}]



def get_answer(question):
    question = str(question) + "\n Response 500 chars maximum: generate short reply. No non-food Qs allowed."
    messages.append({'role': 'user', 'content': question})
    print("[DEBUG] messages: ", question)
    functions = [
    {
        "name": "recipes_recommender",
        "description": """Function to get recipe recommendations based on user specifics (maximum ingredients, steps, preparation time, calories, ingredients to exclude or include and number of desired recipes). All theses specifics are optional, and we can recommend without it.  This function also offers user-unspecific responses for random recommendations.""",
        "parameters": {
            "type": "object",
            "properties": {
                "max_ingredients": {
                    "type": "integer",
                    "description": "Max ingredients of the recipe. Defaults to None.",
                },
                "max_steps": {
                    "type": "integer",
                    "description": "max minutes of the recipe. Defaults to None.",
                },
                "max_minutes": {
                    "type": "integer",
                    "description": "max minutes of the recipe. Defaults to None.",
                },
                "max_calories": {
                    "type": "integer",
                    "description": "max calories of the recipe. Defaults to None.",
                },
                "excluded_ingredient" : {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "list of ingredients to exclude from the recipe. Defaults to None.",
                },
                "included_ingredient" : {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "list of ingredients to include in the recipe. Defaults to None.",
                },
                "number_recipes": {
                    "type": "integer",
                    "description": "number of recipe to fetch. Defaults to None.",
                },

            },
            "required": [],
        },
    },
 
    # We can Add other functions as needed here !!!
]

    response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
    messages=messages,
    functions=functions,
    function_call="auto")
    
    print("[res]", response)
    
    response_message = response.choices[0].message
    

    if response_message.function_call:
        available_functions = {
            'recipes_recommender': recipes_recommender,
        }

        function_name = response_message.function_call.name
        print(function_name)

        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message.function_call.arguments)
        print(function_args)

        function_response = function_to_call(**function_args)
        print(function_response)

        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": str(function_response),
            }
        )

        second_response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=0)  # get a new response from GPT where it can see the function response
        
        messages.append({"role": "assistant", "content": second_response.choices[0].message.content})
        print(second_response.usage)

        return second_response.choices[0].message.content
    else:
        messages.append({"role": "assistant", "content": response_message.content})
        print(response.usage)
        print(messages)
        return response_message.content

if __name__ == '__main__':
