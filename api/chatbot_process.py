import chainlit as cl
import openai_code as openai_code

@cl.on_chat_start
async def start():
    await cl.Message(author="Chatbot", content="""Welcome to RecipeBot! A cook chatbot to give you some recipes and recipe recommendations. ✍️📋

- Search: Search what you want based on a recipe name or key ingredients. 🔍
- Get advice: The chatbot will recommend dishes based on your preferences (tastes, allergies or intolerances)! 💬
                     
What do you want to eat ? 👩‍🍳👨🏾‍🍳               """).send()

@cl.on_message
async def main(message: str):
  
   answer = openai_code.get_answer(message)
   print(message)
   # Send a response back to the user
   await cl.Message(author="Chatbot",
     content=answer,
   ).send()