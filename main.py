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
    

## Cards
blacks = [x.replace("\n","") for x in  open("./black.txt").readlines()]
whites = [x.replace("\n","") for x in  open("./white.txt").readlines()]

userlist = []
card_numer = 5


class User:
    def __init__(self,cards,name,user):
        self.cards = cards
        self.name = name
        self.user = user
        for x in self.cards:
            whites.remove(x)
            
#pinging a bot
@bot.command(aliases = ["p"])
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    embed = discord.Embed(title="Ping", value=f"{ping}", color=discord.Color.red())
    embed.add_field(name=f"{ping}", value="ms")
    embed.set_footer(text="CAH", icon_url="https://wolfyfiles.000webhostapp.com/home/discord/cah.jpg")
    await ctx.send(embed=embed)

# join to game
@bot.command()
async def join(ctx):   
    author=ctx.author
    userlist.append(User(choices(whites,k=card_numer),author.name,author))

    cards = userlist[-1].cards
    #await author.send("Here are your cards:\n\n"+"\n".join(cards))

    cardlist = "\n".join(cards) 
    embed = discord.Embed(title="Üdvözöllek a játékban", color=discord.Color.blue())
    embed.add_field(name = 'Kártyáid:', value=cardlist, inline = True)
    embed.set_footer(text="CAH", icon_url="https://wolfyfiles.000webhostapp.com/home/discord/cah.jpg")
    await author.send(embed=embed)

#list the cards of the user



#list the cards of the user
@bot.command()
async def cards(ctx):
    #await userlist[0].user.send("\n".join(userlist[0].cards))

    cardlist = "\n".join(userlist[0].cards)
    embed = discord.Embed(title="Cards Against Humanity", color=discord.Color.green())
    embed.add_field(name = 'Kártyáid:', value=cardlist, inline = True)
    embed.set_footer(text="CAH", icon_url="https://wolfyfiles.000webhostapp.com/home/discord/cah.jpg")
    await ctx.author.send(embed=embed)

# list all users in the game
@bot.command()
async def users(ctx):
    #await ctx.author.send("\n".join(x.name for x in userlist))

    userl="\n".join(x.name for x in userlist)
    embed = discord.Embed(title="Cards Against Humanity", color=discord.Color.orange())
    embed.add_field(name = 'jelenlegi játékosok:', value=userl, inline = True)
    embed.set_footer(text="CAH", icon_url="https://wolfyfiles.000webhostapp.com/home/discord/cah.jpg")
    await ctx.author.send(embed=embed)

@bot.command(aliases = ["h"])
async def help(ctx):
    embed = discord.Embed(title="Segítség", color=discord.Color.green())
    embed.add_field(name=">help", value="Help menü")
    embed.add_field(name=">join", value="Belépés a játékbai")
    embed.add_field(name=">cards", value="Jelenlegi kártyáid")
    embed.add_field(name=">users", value="Játékban levő játékosok")
    embed.add_field(name=">ping", value="Ping ellenörzés")
    embed.set_footer(text="CAH", icon_url="https://wolfyfiles.000webhostapp.com/home/discord/cah.jpg") 
    await ctx.author.send(embed=embed)


#start the game
@bot.command()
async def start(ctx):
    black_card = choice(blacks)
    print(black_card)
    for user in userlist:
        await user.user.send(black_card)
        await user.user.send("Your cards:\n\n")
        for n,card in enumerate(user.cards):
            await user.user.send(f"[{n}] {card}")

bot.run("")
