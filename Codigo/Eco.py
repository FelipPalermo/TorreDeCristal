import nextcord
import discord
import asyncio
from nextcord.ext import commands 
from Class import Player  

intents = nextcord.Intents.default()
intents.message_content = True 
Eco = commands.Bot(command_prefix="#", intents=intents)

# Show command list ------------------------------------------------------
@Eco.command()
async def commands(ctx):
    await ctx.reply("currently available commands :\n\n #Create - Start your character creation process\n#sstatus - Show your character status\n\
#chp - Add or decrease from HP\n#cmp - add or decrease from mp\n#cname - Change your character name")

# Create character in database ------------------------------------------- 
@Eco.command()
async def create(ctx) :

    if Player.CheckExist(ctx.author.id) == False :

        await ctx.reply("Lets create your character!\nWhat are your attributess?\n\
    Send me like this : Name, Maximum Hp, Maximum MP")

    # check if its the same person sending the message
    # them check the next message to get the attributes
        def check(m : discord.Message) : 
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        
        try :
            msg = await Eco.wait_for("message", check = check, timeout = 60.0)

        except asyncio.TimeoutError : 
            await ctx.send(f"Ei {ctx.author}, não me ignora!\nAgora eu ja esqueci o que te pedi!")
        
        else :
            
                author = ctx.author.id
                msgContent = msg.content
                msgContent = msgContent.split(",")
                msgContent.append(author)

                newPlayer = Player(msgContent)
                await ctx.reply("Thanks, you character has been sucefully created!")

    else :
        await ctx.reply("Hey! You already have a character, you cant be two at once!")

@Eco.command()
async def inv(ctx) :
    
    await user.send_message("Hello")

# Change Status -----------------------------------
# c = change
@Eco.command()
async def chp(ctx) :
    value = ctx.message.content.split(" ")
    ID = ctx.author.id
    Player.Change_Hp(ID, int(value[1])) 

@Eco.command()
async def cmp(ctx) :
    value = ctx.message.content.split(" ")
    ID = ctx.author.id
    Player.Change_Mp(ID, int(value[1])) 

@Eco.command()
async def cname(ctx) : 
    Name = ctx.message.content.split(" ")
    ID = ctx.author.id
    Player.Change_Name(ID, Name)

    await ctx.send("Name changed successfully!")

# Show Status ------------------------------------- 
@Eco.command()
async def sstatus(ctx):
    Status = Player.Show_Inv(ctx.author.id)
    str_Status = "Name : " + Status["Nome"] + "\n" + "Max Hp  : " + str(Status["Vida Maxima"]) + "\n" + "HP : " + str(Status["Hp"]) +  "\n" + "Max Mp : " + str(Status["Mana Maxima"]) +  "\n" + "Mp : " + str(Status["Mp"]) +  "\n" + "Corruption  : " + str(Status["Corrupcao"])

    embed = discord.Embed(
            colour = discord.Colour.dark_purple(),
            title = "Status",
            description = str_Status)

    embed.set_thumbnail(url="https://i.imgur.com/TyFTbsY.png")
    await ctx.reply(embed=embed)











# Conexao ------------------------------
Token = "MTEwMjI0MjEyNDI2ODgzMDgyMQ.Gj_MTa.JKGLb8oMF6P0veqsyWDd6CtCptNFKEUtwmSXSE"

Eco.run(Token)

# -------------------Ideias------------------------

# Trocar a pesquisa de "nome" para "discordID", como verificacao de seguranca
# para cada jogador conseguir alterar apenas a propria ficha

# Adicionar um comando para receber o ID do mestre e ele poder alterar todos os personagens


