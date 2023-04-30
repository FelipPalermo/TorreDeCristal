import nextcord
import discord
import asyncio
from nextcord.ext import commands 
from Class import Player  

intents = nextcord.Intents.default()
intents.message_content = True 
Eco = commands.Bot(command_prefix="#", intents=intents)

@Eco.command()
async def criar(ctx) :
    await ctx.reply("Vamos criar seu personagem!\nQuais são seus atributos?\n\
   Modelo : Nome, vida maxima, mana maxima, corrupcao")

# checa se a mesma pessoa que mandou a menssagem antes esta mandando agora
# Pegar proxima menssagem do autor para fazer o personagem
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
        await ctx.reply("Obrigado, você foi criado com sucesso!")






# Conexao ------------------------------
Token = "MTEwMjI0MjEyNDI2ODgzMDgyMQ.GCOMa7.wDMSgtAoVxmhAprUZr1GsLZAksjk27PdyfdFeM"

Eco.run(Token)
