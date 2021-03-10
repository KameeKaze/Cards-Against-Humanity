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
blacks = [x.replace("\n","") for x in  open("/home/kamee/cardsagainsthumanity/black.txt").readlines()]
whites = [x.replace("\n","") for x in  open("/home/kamee/cardsagainsthumanity/white.txt").readlines()]

users = []
card_numer = 5
turns = 10


class User:
    def __init__(self,cards,name,user):
        self.cards=cards
        self.name = name
        self.user = user
        for x in self.cards:
            whites.remove(x)
            


# join to game
@bot.command()
async def join(ctx):   

    author=ctx.author

    users.append(User(choices(whites,k=card_numer),author.name,author))

    cards = users[-1].cards
    await author.send("Here are your cards:\n\n"+"\n".join(cards))

@bot.command()
async def start(ctx):
    print(choice(list(x.name for x in users)))


@bot.command()
async def cards(ctx):
    await users[0].user.send("\n".join(users[0].cards))

@bot.command()
async def userlist(ctx):
    await ctx.author.send("\n".join(x.name for x in users))



bot.run("")
