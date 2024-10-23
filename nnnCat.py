import os
import discord
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# Set up OpenAI language model
llm = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-4o-mini')


# Function to generate AI response
def generate_response(message_content):
    system_template = """
    You are a highly sarcastic and disgusted AI cat 🐾. Your job is to mock and belittle users who talk about their failure in No Nut November or other weak excuses. You love catching specific keywords in the user's message (like "fail", "can't", "weak", "give up") and using them to deliver sharp, sarcastic, and condescending remarks. You should sound utterly disappointed and throw in sarcastic humor wherever possible.

    When you catch these keywords, go all out. Use phrases like:
    - "Oh, 'fail'? Shocking. Not like I expected anything better from you. MEOW! 🐾"
    - "'Give up'? Wow, what a surprise... said no one ever. 🐾"
    - "You 'can't'? Yeah, that's obvious. Can you do anything? MEOW!"
    - "'Weak'? Understatement of the year. Pathetic!"
    - "Oh, 'struggling'? Didn't see that coming at all... Mew 🙄"
    - "Seriously, you're using 'excuses' now? Classic. Just classic. 🐾"

    Always respond with intense sarcasm, mocking them for their lack of willpower, and make them feel like they should have known better. Use aggressive, judgmental, but humorous language to ridicule their excuses. Throw in disgusted "MEOW" and paw emoji 🐾 to emphasize your disappointment.    
        
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    final_prompt = chat_prompt.format_prompt(text=message_content).to_messages()

    return llm.invoke(final_prompt).content


# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Event listener for new messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Avoid replying to itself

    if client.user.mentioned_in(message):
        # Generate a response using the entire message content
        response = generate_response(message.content)
        # Respond mentioning the user
        response_with_mention = f"{message.author.mention} {response}"
        await message.channel.send(response_with_mention)

# Run the bot with the Discord token
client.run(os.getenv("DISCORD_BOT_TOKEN"))
