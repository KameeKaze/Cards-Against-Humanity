#/bin/python3
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
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
reactions = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"] # if you wanna play with more cards, add the emojies
icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Cards_Against_Humanity_logo.png/220px-Cards_Against_Humanity_logo.png"

class User:
    score = 0
    current_card= None
    def __init__(self,cards,name,user):
        self.cards = cards
        self.name = name
        self.user = user
        for x in self.cards:
            whites.remove(x)
            
#ping command
@bot.command(aliases = ["p"])
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    embed = discord.Embed(title="Ping", value=f"{ping}", color=discord.Color.gold())
    embed.add_field(name=f"{ping}", value="ms")
    embed.set_footer(text="CAH", icon_url=icon)
    await ctx.send(embed=embed)


#join to the game
@bot.command(aliases = ["j"])
async def join(ctx):
    author=ctx.author

    # check if user already joined
    if all([x.user != author for x in userlist]):
        # create new user
        userlist.append(User(choices(whites,k=card_numer),author.name,author))

        # get the new user's cards
        cards = "\n".join(userlist[-1].cards) 

        # send join message and cards
        embed = discord.Embed(title="Wellcome to the game", color=discord.Color.gold())
        embed.add_field(name = 'Your cards:', value=cards, inline=True)
        embed.set_footer(text="CAH", icon_url=icon)
        await author.send(embed=embed)

    #error if user already joined
    else:await author.send(embed=discord.Embed(title="You've already joined to the game", color=discord.Color.red()))

#list your cards
@bot.command(aliases = ["card", "c"])
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
@bot.command(aliases = ["user", "u"])
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
    embed.add_field(name=">start", value="Start the game", inline=False)
    embed.add_field(name=">help", value="Give this help list", inline=False)
    embed.add_field(name=">join", value="Join to the game", inline=False)
    embed.add_field(name=">cards", value="Your current cards", inline=False)
    embed.add_field(name=">users", value="Users in game", inline=False)
    embed.add_field(name=">ping", value="Checks the ping", inline=False)
    embed.set_footer(text="CAH", icon_url=icon) 
    await ctx.author.send(embed=embed)

#send message
async def message(member):
    embed = discord.Embed(title=black_card,color=discord.Color.gold())
    for n,card in enumerate(member.cards):            
        embed.add_field(name=f"[{n+1}]",value=card, inline=False)
    embed.set_footer(text="CAH", icon_url=icon)
    return await reactionadd(await member.user.send(embed=embed))
    
#put reactions on the messages
async def reactionadd(msg):
    for emoji in reactions:
        await msg.add_reaction(emoji)
    return msg
    
#checks if all users voted
async def isvoted(msg):
    msg = await msg.channel.fetch_message(msg.id)
    return all([x.count == 1 for x in msg.reactions]) # returns true if some users havent voted
    

#start the game
@bot.command(aliases = ["s"])
async def start(ctx):
    #checks if author is a joined user
    if any([x.user == ctx.author for x in userlist]):

        #draw a black card
        global black_card
        black_card = choice(blacks)
        blacks.remove(black_card)
        #send messages to all users
        messages = await asyncio.gather(*map(message,userlist))
        # wait for all user's vote
        while all(await asyncio.gather(*map(isvoted,messages))):
            pass


    else:
        await ctx.author.send(embed=discord.Embed(title="You aren't joined. Type: **>join**", color=discord.Color.red())) # send warning to join 



@bot.command()
async def scoreboard(ctx):
    pass 
#todo later

TOKEN = open("./token.txt",'r').read().replace("\n","")
bot.run(TOKEN)



async def isvoted(msg):
    if all([emoji.count == 1 for emoji in msg.reactions]):
        return False
    else:
        return True


