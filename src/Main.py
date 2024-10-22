#IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord

# Other imports
from discord.ext import commands
import random
import catapi
import asyncio

import os
from dotenv import load_dotenv

load_dotenv()

CAT_API_KEY = os.getenv('CAT_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')



#GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.

# bot = discord.Client(intents=discord.Intents.all())

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

api = catapi.CatApi(api_key=CAT_API_KEY)

 #EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print(bot.guilds)

 #EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.

@bot.event
async def on_message(message):

    # Convert message string into list of words
    list = message.content.split()

    # Ignore posts from itself, no spam
    if message.author == bot.user:
        return

    # If the message length was greater than 25, scold the author for yapping
    if len(list) > 25:
        await message.channel.send("bro quit yapping, you literally said " + str(len(list)) +  " words right there")

    # If the author mentions the words "sad", "sucks", "rough", "depressed", "terrible"
    # Cheer them up with a cat poster
    for word in list:
        if word == "sad" or word == "sucks" or word == "rough" or word == "depressed" or word == "terrible":
            await message.channel.send("Hey, cheer up! You'll get through this!")
            await message.channel.send("https://i.pinimg.com/originals/69/98/39/6998396b8c4fc79607712af48b5e41c9.jpg")

    # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
    if message.content == "hello":
        # SENDS BACK A MESSAGE TO THE CHANNEL.
        await message.channel.send("hello kind sir")

    # processes command-type events    
    await bot.process_commands(message)

    # Checks message id. If message id modulo 10 = 0, respond to message with missing cat poster.
    if message.id % 10 == 0:
        name = list[random.randrange(0, len(list))]
        name = name.capitalize()
        await message.channel.send("Hi, have you seen my cat? He's missing. He'll respond to \"" + name + "\". " + "He looks like this:")
        response = await api.search_images(format="json", limit="1", size="small")
        await message.channel.send(response[0].url)


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def cat_image(ctx):
    response = await api.search_images(format="json", limit="1", size="small")
    await ctx.send(response[0].url)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

bot.run(BOT_TOKEN)
