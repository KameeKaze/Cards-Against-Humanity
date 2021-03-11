#/bin/python3
import discord
from discord.ext import commands
from random import choices
from random import choice

bot = commands.Bot(command_prefix=">")
bot.remove_command('help') # own help menu near to the end

@bot.event
async def on_ready():
    print("I'm ready!")

## import cards
blacks = [x.replace("\n","") for x in  open("./black.txt").readlines()]
whites = [x.replace("\n","") for x in  open("./white.txt").readlines()]

userlist = []
card_numer = 5
icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Cards_Against_Humanity_logo.png/220px-Cards_Against_Humanity_logo.png"

class User:
    def __init__(self,cards,name,user):
        self.cards = cards
        self.name = name
        self.user = user
        for x in self.cards:
            whites.remove(x)
            
#bot pings
@bot.command(aliases = ["p"])
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    embed = discord.Embed(title="Ping", value=f"{ping}", color=discord.Color.gold())
    embed.add_field(name=f"{ping}", value="ms")
    embed.set_footer(text="CAH", icon_url=icon)
    await ctx.send(embed=embed)

#join to the game
@bot.command()
async def join(ctx):   
    # create new user
    author=ctx.author
    userlist.append(User(choices(whites,k=card_numer),author.name,author))


    cards = "\n".join(userlist[-1].cards) # get the new user's cards

    # send join message and cards
    embed = discord.Embed(title="Wellcome to the game", color=discord.Color.gold())
    embed.add_field(name = 'Your cards:', value=cards, inline=True)
    embed.set_footer(text="CAH", icon_url=icon)
    await author.send(embed=embed)

#list your cards
@bot.command()
async def cards(ctx):
    # get the user
    for user in userlist:
        if ctx.author.name == user.name:
            break
    # get the user's cards and send
    cards = "\n".join(user.cards)
    embed = discord.Embed(title="Cards Against Humanity", color=discord.Color.gold())
    embed.add_field(name = 'Your cards:', value=cards, inline=True)
    embed.set_footer(text="CAH", icon_url=icon)
    await ctx.author.send(embed=embed)

# list all users in the game
@bot.command()
async def users(ctx):
    userl="\n".join(x.name for x in userlist)
    embed = discord.Embed(title="Cards Against Humanity", color=discord.Color.gold())
    embed.add_field(name = 'Users in game:', value=userl, inline=True)
    embed.set_footer(text="CAH", icon_url=icon)
    await ctx.author.send(embed=embed)

#help menu
@bot.command(aliases = ["h"])
async def help(ctx):
    embed = discord.Embed(title="Help", color=discord.Color.gold())
    embed.add_field(name=">help", value="Give this help list", inline=False)
    embed.add_field(name=">join", value="Join to the game", inline=False)
    embed.add_field(name=">cards", value="Your current cards", inline=False)
    embed.add_field(name=">users", value="Users in game", inline=False)
    embed.add_field(name=">ping", value="Checks the ping", inline=False)
    embed.set_footer(text="CAH", icon_url=icon) 
    await ctx.author.send(embed=embed)

#start the game
@bot.command()
async def start(ctx):
    #draw a black card
    black_card = choice(blacks)
    blacks.remove(black_card)
    #enumerate users
    for user in userlist:
        embed = discord.Embed(title=black_card,color=discord.Color.gold())
    #enumerate user's cards
        for n,card in enumerate(user.cards):            
            embed.add_field(name=f"[{n+1}]",value=card, inline=False)
    #send black cards and user's cards
        embed.set_footer(text="CAH", icon_url=icon)
        await user.user.send(embed=embed)
        

bot.run("")
