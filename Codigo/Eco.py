import nextcord
import discord
import asyncio
import random
from nextcord.ext import commands 
from Class import Player 
from ServerDB import Server

intents = nextcord.Intents.default()
intents.message_content = True 
Eco = commands.Bot(command_prefix="#", intents=intents)


# Show command list ------------------------------------------------------
@Eco.command()
async def Help(ctx):

    embed = discord.Embed(
            colour = discord.Colour.dark_purple(),
            title = "Status",
            description = "#create - create a new character\n#status - show your character status\n#chp  (5 or -5) - change hp\n#cmp (5 or -5) - change mp\n#cname (new name) - change character name\n#cimage (imageURL) - Change your character image")

    embed.set_thumbnail(url="https://i.imgur.com/8mPrGNU.png")
    await ctx.reply(embed=embed, delete_after=20)

    if Server.RAntiFlood(ctx.guild.id) == True : await ctx.message.delete()

# Anti flood control ----------------------------------------------------
@Eco.command()
async def antiflood(ctx) :
    Server.AntiFlood(ctx.guild.id)
    

    if Server.RAntiFlood(ctx.guild.id) == True :  
        await ctx.reply("Anti flood is ON", delete_after=5)

    else :
        await ctx.reply("Anti flood is OFF")

    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Create Database for guild ---------------------------------------------
@Eco.command()
@commands.has_any_role("admin", "Admin", "GM", "moderator")
async def create_game_DB(ctx):

    try :

        Player.newDB(ctx.guild.id) 
        NewServerCol = Server(["pt-br", str(ctx.author.id)])

        await ctx.reply("Succefully created database!", delete_after=5)

    except :

        await ctx.reply("Dabatase already exists!", delete_after=5)
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Delete Database of the guild -------------------------------------------
@Eco.command()
@commands.has_any_role("admin", "Admin", "GM", "moderator")
async def delete_game_DB(ctx):

        try : 
            Player.deleteDB(ctx.guild.id)
            await ctx.reply("Database deleted!", delete_after=5)
        
        except :
            await ctx.reply("please contact the bot creator to verify this error")
        if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Create character in database ------------------------------------------- 
@Eco.command()
async def create(ctx) :
    
    
    if Player.Return_DBNames(ctx.guild.id) == True :
        if Player.CheckExist(str(ctx.author.id), str(ctx.guild.id)) == False :

            await ctx.reply("Lets create your character!\nWhat are your attributess?\n\
    Send me like this : Name, Maximum Hp, Maximum MP", delete_after=10)

        # check if its the same person sending the message
        # them check the next message to get the attributes
            def check(m : discord.Message) : 
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            
            try :
                msg = await Eco.wait_for("message", check = check, timeout = 60.0)

            except asyncio.TimeoutError : 
                await ctx.send(f"Ei {ctx.author}, não me ignora!\nAgora eu ja esqueci o que te pedi!")
            
            else :
               
                # Gettign user and guild ID 
                    author = ctx.author.id
                    authorGuild_ID = ctx.guild.id
                    msgContent = msg.content
                    msgContent = msgContent.split(",")

                    msgContent.append(str(author))
                    msgContent.append(str(authorGuild_ID))
                    

                    newPlayer = Player(msgContent)
                    await ctx.reply("Thanks, you character has been sucefully created!", delete_after=3)

        else :
            await ctx.reply("Hey! You already have a character, you cant be two at once!", delete_after=10)
    else : 
        await ctx.reply("Your server do not have an dedicated database, please ask an moderator to use \"#create_game_DB\"", delete_after=10)
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

@Eco.command()
async def inv(ctx) :
    
    await user.send_message("Hello")

# Change Hp ----------------------------------------
@Eco.command()
async def chp(ctx) :
 
    value = ctx.message.content.split(" ")
    ID = ctx.author.id
    Player.Change_Hp(ID, ctx.guild.id, int(value[1])) 
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Change Max Hp ----------------------------------------
@Eco.command()
@commands.has_any_role("admin", "Admin", "GM", "moderator")
async def cMhp(ctx) :

    value = ctx.message.content.split(" ")
    Player.Change_MaxHp(ctx.author.id, ctx.guild.id, int(value[1]))
    Player.Change_Hp(ctx.author.id, ctx.guild.id, 1)
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Change Max Mp ------------------------------------------
@Eco.command()
@commands.has_any_role("admin", "Admin", "GM", "moderator")
async def cMmp(ctx) :

    value = ctx.message.content.split(" ")
    Player.Change_MaxMp(ctx.author.id, ctx.guild.id, int(value[1]))
    Player.Change_Mp(ctx.author.id, ctx.guild.id, 1)  
    await ctx.message.delete()
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

#Change mana -----------------------------------------
@Eco.command()
async def cmp(ctx) :

    value = ctx.message.content.split(" ")
    ID = ctx.author.id
    Player.Change_Mp(ID, ctx.guild.id, int(value[1])) 
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Change name ---------------------------------------
@Eco.command()
async def cname(ctx) : 
    
    Name = ctx.message.content.split(" ")
    ID = ctx.author.id
    Player.Change_Name(ID, ctx.guild.id, Name)

    await ctx.send("Name changed successfully!",delete_after=3)
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Change image -------------------------------------
@Eco.command()
async def cimage(ctx):
    
    message = ctx.message.content.split(" ")
    Player.cimage(ctx.author.id, ctx.guild.id, message[1]) 
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Show Status ------------------------------------- 
@Eco.command()
async def status(ctx):
    Status = Player.Show_Status(ctx.author.id, ctx.guild.id)

    # Refazer esse desing para algo automatico
    str_Status = "Name : " + Status["Name"] + "\n" + "Max Hp  : " + str(Status["Maximum life"]) + "\n" + "HP : " + str(Status["Hp"]) +  "\n" + "Max Mp : " + str(Status["Maximum mana"]) +  "\n" + "Mp : " + str(Status["Mp"]) +  "\n" + "Corruption  : " + str(Status["Corruption"])

    embed = discord.Embed(
            colour = discord.Colour.dark_purple(),
            title = "Status",
            description = str_Status)

    embed.set_thumbnail(url=Player.Rimage(ctx.author.id, ctx.guild.id))
    await ctx.reply(embed=embed, delete_after=15)
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()

# Roll dice ---------------------------------------------------------------
@Eco.command()
async def d(ctx):

    images = ["https://i.imgur.com/EA7tYOm.png", "https://i.imgur.com/xY4gUyW.png"] 

    Dice_Faces = ctx.message.content.split(" ")
    Dice_Faces = Dice_Faces[1]

    Roll = random.randint(1, int(Dice_Faces)) 
    
    if Roll > int(Dice_Faces) / 2 :
        message = "🎲 : " + str(Roll) 
        images = images[0]
        
    else : 
        message = "🎲 : " + str(Roll)
        images = images[1]

    embed = discord.Embed(
            colour = discord.Colour.dark_purple(),
            title = "Dice result",
            description = message)

    embed.set_thumbnail(images)

    await ctx.reply(embed=embed, delete_after=15)
    if Server.RAntiFlood(ctx.guild.id)  == True : await ctx.message.delete()



# Conexao ------------------------------
Token = "MTEwMjI0MjEyNDI2ODgzMDgyMQ.Gk_GyS.nV-Gx3Be2uIfYtWc2kcJ9EZezTCidxSv-s2tTo"

Eco.run(Token)

# -------------------Ideias------------------------


# Um comando para inicializar o bot em um servidor e fazer ele criar um banco de dados baseado servidor
# assim permitindo que um jogador tenha mais de um personagem em varios servidores 

# Adicionar um comando para receber o ID do mestre e ele poder alterar todos os personagens


