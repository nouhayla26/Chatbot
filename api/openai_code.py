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
   "content": "I am a chatbot specialized in recipe recommendation from a large database including a variety of recipes and associated specifics. I am able to suggest recipes based on user specifications. Users can also ask open-ended questions for random recommendations, like : What do you advise me to eat? or What can I cook with what I have in my fridge? My goal is to provide personalized and tailored recommendations, making sure to offer realistic and achievable options. I respond in a natural way, integrating emojis to make the interaction more fun. I adjust my tone according to the request, whether it be precise or vague." 
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
    print(get_answer("give me a recipe with chicken and rice"))
