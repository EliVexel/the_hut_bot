import requests
from util import send_embed_message
from discord.ext import commands
import discord
import random


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description="Gives out a random meme")
    async def meme(self, ctx):
        json_data = requests.get("https://meme-api.herokuapp.com/gimme").json()
        await send_embed_message(
            ctx=ctx, content=f"r/{json_data['subreddit']}\n{json_data['postLink']}", title=json_data['title'], image_url=json_data['url'])
    
    @commands.command(name="dadjoke", description="Gives out a random dad joke")
    async def dad_joke(self, ctx):
        headers = {'Accept': 'text/plain'}
        await ctx.send(requests.get("https://icanhazdadjoke.com/", headers=headers).text)

    @commands.command(description="Gives out a random yes/no/maybe image")
    async def yesno(self, ctx, *args):
        data = requests.get("https://yesno.wtf/api/").json()
        await send_embed_message(ctx=ctx, image_url=data["image"])
    
    @commands.command(description="Generates a be like bill image given gender value, which can be F or M for Female or Male")
    async def blb(self, ctx, user : discord.Member = None, gender='M'):
        if user:
            name = user.name
        else:
            name = ctx.message.author.name
        
        name = name.replace(" ", "%20")
        sex = gender.lower()
        await send_embed_message(ctx=ctx, image_url=f"https://belikebill.ga/billgen-API.php?default=1&name={name}&sex={sex}")

    @commands.command(description="Gives out a random star wars quote")
    async def swq(self, ctx):
        data = requests.get("http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote").json()
        await send_embed_message(ctx=ctx, content=data['starWarsQuote'])
    
    @commands.command(description="Gives out a random xkcd comic")
    async def xkcd(self, ctx):
        max_num = requests.get("https://xkcd.com/info.0.json").json()["num"]
        random_comic_num = random.randint(1, max_num)
        data = requests.get(f"https://xkcd.com/{random_comic_num}/info.0.json").json()["img"]
        await send_embed_message(ctx=ctx, image_url=data)

    @commands.command(description="Gives out a random company buzzword")
    async def buzzword(self, ctx):
        await ctx.send(requests.get("https://corporatebs-generator.sameerkumar.website/").json()["phrase"])

def setup(bot):
    bot.add_cog(Meme(bot))
