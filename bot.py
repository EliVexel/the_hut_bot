# -*- coding: utf-8 -*-
from discord.ext import tasks, commands
from CoronaData.corona_virus_updater import update_data, get_corona_news
import datetime

bot = commands.Bot(command_prefix="h!")

startup_extensions = ["gen", "gladiator", "meme", "trivia", "corona"]

for extension in startup_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

 # update corona virus data every x mins


@tasks.loop(hours=0.1)
async def corona_update_task():
    print("Updating coronavirus data")
    update_data()
    print("Updated coronavirus data")


@tasks.loop(hours=0.1)
async def corona_update_news_task():
    news = get_corona_news()
    channel = bot.get_channel(688045137162666051)
    if news:
        for k in news:
            await channel.send(k)


@bot.event
async def on_ready():
    print(f"Connected!\nName: {bot.user.name}\nId: {bot.user.id}\n")
    corona_update_task.start()
    corona_update_news_task.start()


try:
    import bot_token
    bot.run(bot_token.token())
except ModuleNotFoundError:
    import os
    bot.run(os.environ['BOT_TOKEN'])
