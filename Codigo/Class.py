from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://FelipePalermo:ApiKey@torredecristal.zvmqwjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

Player_Data = client["Players"].get_collection("Player_Data")


# Classe Personagem ----------------------------------------

class Player :

    def __init__(self, atr) :

        self.Nome = atr[0].lower()
        self.Vida_Maxima = int(atr[1])
        self.Hp = int(atr[1])
        self.Mana_Maxima = int(atr[2])
        self.Mana = int(atr[2])
        self.Corrupcao = 0
        self.DiscordID = atr[3]
        self.DiscordGuildID = atr[4]

        # Return a list with the player status
        self.PlayerStats = list(Player_Data.find({"Nome" : self.Nome}).limit(1)) 
        
        if client[str(self.DiscordGuildID)].Players.count_documents({"DiscordID" : self.DiscordID}) >= 1 :
            pass

        else :

            client[str(self.DiscordGuildID)].Players.insert_one({

                "GuildID" : self.DiscordGuildID,
                "DiscordID" : self.DiscordID,
                "Name" : self.Nome,
                "Maximum life" : self.Vida_Maxima,
                "Hp" : self.Hp,
                "Maximum mana" : self.Mana_Maxima,
                "Mp" : self.Mana, 
                "Corruption" : self.Corrupcao,
                "ImageUrl" : ""})


# Return Players collection ---------------------------------------------------------------------------------------
    @staticmethod
    def Return_Guild(GuildID) :
        Db = client[str(GuildID)].get_collection("Players")
        return Db

# Return All database names ---------------------------------------------------------------------------
    @staticmethod
    def Return_DBNames(GuildID) :
        dbnames = client.list_database_names()

        if str(GuildID) in dbnames :
            return True

        else :
            return False 

# Check if player document exists -----------------------------------------------------------------------------------------
    @staticmethod
    def CheckExist(DiscordID, GuildID) :
        
        if Player.Return_Guild(GuildID).count_documents({"DiscordID" : DiscordID}) >= 1 :
            return True
        else :
            return False

# Delete character ---------------------------------------------------------------------------    
    @staticmethod 
    def DelChar(nome) : 
        filtro = {"Nome" : nome}
        Player_Data.delete_one(filtro)
     
# HP -----------------------------------------------------------------------------------------
    @staticmethod
    def Change_MaxHp(DiscordID, GuildID, value) : 
        Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$inc" : {"Maximum life" : value}})
 
    @staticmethod
    def Change_Hp(DiscordID, GuildID, value) : 
        PlayerStats =  list(Player.Return_Guild(GuildID).find({"DiscordID" : str(DiscordID)}).limit(1))

       # If the value is greathr than the maxium hp, the hp goes to the maxium
        if value + PlayerStats[0]["Hp"] > PlayerStats[0]["Maximum life"] :
            Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$set" : {"Hp" : PlayerStats[0]["Maximum life"]}})
         
        else :
            Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$inc" : {"Hp" : value}})
       
        # Prevent from hp be less than 0
        if value + PlayerStats[0]["Hp"] <= 0:
            Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$set" : {"Hp" : 0}})

# MP -----------------------------------------------------------------------------------------
    @staticmethod
    def Change_MaxMp(DiscordID, GuildID, value) : 
        Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$inc" : {"Maximum mana" : value}})
    
    @staticmethod
    def Change_Mp(DiscordID, GuildID ,value) : 
        PlayerStats =  list(Player.Return_Guild(GuildID).find({"DiscordID" : str(DiscordID)}).limit(1))

       # if the value is greater than maxium Mp, Mp goes to the maxium
        if value + PlayerStats[0]["Mp"] > PlayerStats[0]["Maximum mana"] :
            Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$set" : {"Mp" : PlayerStats[0]["Maximum mana"]}})

        else :
            Player.Return_Guild(GuildID).update_one({"DiscordID" : str(DiscordID)}, {"$inc" : {"Mp" : value}})

        # Prevent from Mp be less than 0
        if value + PlayerStats[0]["Mp"] <= 0:
            Player.Return_Guild(GuildID).update_one({"DiscordID" : DiscordID}, {"$set" : {"Mp" : 0}})

# Corruption -----------------------------------------------------------------------------------
    @staticmethod
    def Change_Corrupt(DiscordID, value) : 
        Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Coruption" : value}})


# Change name ----------------------------------------------------------------------------------
    @staticmethod
    def Change_Name(DiscordID, Name) :
        if len(Name) > 2:

            # If name array is greater than 2
            # exclude word"cname" and cast the list to string
            New_Name = " ".join(Name[1::])
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Name" : New_Name}})

        else : 
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Name" : Name[1]}})

# Add or change image --------------------------------------------------------------------------
    @staticmethod
    def cimage(DiscordID, GuildID, ImageUrl) :

        Player.Return_Guild(str(GuildID)).update_one({"DiscordID" : str(DiscordID)}, {"$set" : {"ImageUrl" : ImageUrl}})

# Return image character image ---------------------------------------------------------------------------------- 
    @staticmethod
    def Rimage(DiscordID, GuildID) :   
        PlayerStats =  list(Player.Return_Guild(GuildID).find({"DiscordID" : str(DiscordID)}).limit(1))

        if PlayerStats[0]["ImageUrl"] == "" :
            return "https://imgur.com/3be00df2-3ce0-4e04-8a51-c2a23f643219"

        return str(PlayerStats[0]["ImageUrl"])

# Create new database for server ----------------------------------------------------------------
    @staticmethod
    def newDB(GuildID) : 
        newDB = client[str(GuildID)]
    
        PlayerCol = newDB.create_collection("Players") 
        InvCol = newDB.create_collection("Inventory")

# Delete server database ------------------------------------------------------------------------ 
    @staticmethod
    def deleteDB(GuildID) :
        client.drop_database(str(GuildID))

# Show -----------------------------------------------------------------------------------------
    @staticmethod
    def Show_Status(DiscordID, GuildID) : 
        PlayerStats =  Player.Return_Guild(GuildID).find_one({"DiscordID" : str(DiscordID)})

        return PlayerStats

    @staticmethod
    def Show_Inv(DiscordID) :
        pass



# when using DiscordID convert it to string
# GuildID is returned as INT, for comparations in collections cast to STRING 
