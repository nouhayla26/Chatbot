import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message(author="Chatbot", content="""Welcome to RecipeBot! A cook chatbot to give you some recipes and recipe recommendations. ✍️📋

- Search: Search what you want based on a recipe name or key ingredients. 🔍
- Get advice: The chatbot will recommend dishes based on your preferences (tastes, allergies or intolerances)! 💬
                     
What do you want to eat ? 👩‍🍳👨🏾‍🍳               """).send()

@cl.on_message
async def main(message: str):
   # Your custom logic goes here…
   # Send a response back to the user
   await cl.Message(author="Chatbot",
     content="------------------TO DO------------------",
   ).send()