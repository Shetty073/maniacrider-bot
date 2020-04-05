import discord, json
from discord.ext import commands
from configparser import ConfigParser


# Get the data from config file
config = ConfigParser()
config.read('config.ini')
BOT_TOKEN = config['BOT']['token']


# Bot code begins from here
bot = commands.Bot(command_prefix='.', description="Type `.help` for help", case_insensitive=True)


# Remove the default help command
bot.remove_command("help")


@bot.event
async def on_ready():
    print("ManiacRider online")
    await bot.change_presence(activity=discord.Game("Type `.help` for help"))

@bot.event
async def on_message(msg):
    message = msg.content.lower()
    author = msg.author.name
    ch = msg.channel

    # do something with that message
    replies = {
        "hi": "Hi", 
        "good night": f"Good night {author}", 
        "gn": f"Good night {author}",
        "good morning": f"Good morning {author}", 
        "gm": f"Good morning {author}",
        "good evening": f"Good evening {author}", 
        "ge": f"Good evening {author}",
        "good day": f"Good day {author}", 
        "gd": f"Good day {author}",
        "help": "Please type `.help` for the help menu"
        }
    if message in replies.keys():
        await ch.send(replies[f"{message}"])
    # process commands along with messages
    await bot.process_commands(msg)


# Help menu
@bot.command()
async def help(ctx):
    with open("help.json", 'r') as f:
        ask_content = json.load(f)
    help_str = ""
    for k, v in ask_content.items():
        help_str += f"**{k}**: {v}\n"
    help_embed = discord.Embed(
        title=":palm_tree:/ : \\\:palm_tree:",
        type="rich",
        description="Always ride with proper gear :helmet_with_cross:",
        colour=discord.Colour.gold()
    )
    help_embed.set_author(name=f"Live to ride bois..",
                         icon_url="https://i.imgur.com/8SWg2NH.jpg")
    help_embed.add_field(name="Commands",
                        value=f"{help_str}\n\n", inline=False)
    async with ctx.channel.typing():
        await ctx.send(embed=help_embed)


# cogs list
extensions = ["cogs.fetch"]


# load all cogs
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"{extension} extension loaded..")
        except Exception as e:
            print(f"ERROR: cannot load extension {extension} \n{e}")

bot.run(BOT_TOKEN)
