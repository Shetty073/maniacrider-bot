import discord
from discord import Embed, Color
from discord.ext import commands
from configparser import ConfigParser
import requests, json


class FetchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def fetch(self, ctx, *, model_name=""):
        if model_name == "":
            async with ctx.channel.typing():
                await ctx.send("name of the bike is a required argument")
        else:
            # do something
            request_url = "http://127.0.0.1:5000/bike/specs/" + model_name
            resp = requests.get(request_url)
            if resp.status_code != 200:
                async with ctx.channel.typing():
                    await ctx.send("API server down! notify developer")
            else:
                data = json.loads(resp.content)
                if data is None:
                    async with ctx.channel.typing():
                        await ctx.send("Bike not found\nThere are 2 possible reasons: \n1. Data for this bike might not have been added into the server (in which case check back in a few weeks)\n2. Typo or punctuation error in model_name provided")
                else:
                    keys_for_deletion = []
                    for k, v in data.items():
                        if v is None:
                            keys_for_deletion.append(k)
                    for k in keys_for_deletion:
                        del data[k]
                    bike_pic = data["Bike Picture"]
                    bike_name = data["Model Name"].title()
                    bike_price = data["Bike Price"]
                    del data["Bike Picture"]
                    del data["Model Name"]
                    del data["Bike Price"]
                    specs = "__**Features and Specifications**__: \n"
                    for k, v in data.items():
                        specs += f"**{k}**: {v}\n"
                    
                    # Preapare an Embed
                    specs_embed = Embed(
                        title=bike_name,
                        type="rich",
                        description=f"Price: {bike_price}",
                        colour=Color.magenta()
                    )
                    specs_embed.set_author(name=f"Showing stats of {bike_name}")
                    specs_embed.set_image(url=bike_pic)
                    specs_embed.add_field(name="All prices are ex-showroom Delhi", value=specs, inline=False)
                    async with ctx.channel.typing():
                        await ctx.send(embed=specs_embed)


def setup(bot):
    bot.add_cog(FetchCog(bot))
