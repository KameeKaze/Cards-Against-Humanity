#/bin/python3
import discord
from discord.ext import commands
from random import choices
from random import choice

bot = commands.Bot(command_prefix=">")

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
            


# join to game
@bot.command()
async def join(ctx):   
    author=ctx.author
    userlist.append(User(choices(whites,k=card_numer),author.name,author))

    cards = userlist[-1].cards
    await author.send("Here are your cards:\n\n"+"\n".join(cards))



#list the cards of the user
@bot.command()
async def cards(ctx):
    await userlist[0].user.send("\n".join(userlist[0].cards))

# list all users in the game
@bot.command()
async def users(ctx):
    await ctx.author.send("\n".join(x.name for x in userlist))


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