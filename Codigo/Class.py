from pymongo.mongo_client import MongoClient
uri = ""
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

        # Return a list with the player status
        self.PlayerStats = list(Player_Data.find({"Nome" : self.Nome}).limit(1)) 
        
        if Player_Data.count_documents({"DiscordID" : self.DiscordID}) >= 1 :
            pass

        else :

            Player_Data.insert_one({

                "DiscordID" : self.DiscordID,
                "Nome" : self.Nome,
                "Vida Maxima" : self.Vida_Maxima,
                "Hp" : self.Hp,
                "Mana Maxima" : self.Mana_Maxima,
                "Mp" : self.Mana, 
                "Corrupcao" : self.Corrupcao})

# Check Exist ---------------------------------------------------------------------------------
    @staticmethod
    def CheckExist(DiscordID) :

        if Player_Data.count_documents({"DiscordID" : DiscordID}) >= 1 :
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
    def Change_MaxHp(DiscordID, value) : 
        Player_Data.update_one({"DiscordID" : DiscordID}, {"$inc" : {"Vida Maxima" : value}})

    @staticmethod
    def Change_Hp(DiscordID, value) : 
        PlayerStats =  list(Player_Data.find({"DiscordID" : DiscordID}).limit(1))

       # If the value is greathr than the maxium hp, the hp goes to the maxium
        if value + PlayerStats[0]["Hp"] > PlayerStats[0]["Vida Maxima"] :
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Hp" : PlayerStats[0]["Vida Maxima"]}})
         
        else :
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$inc" : {"Hp" : value}})
       
        # Prevent from hp be less than 0
        if value + PlayerStats[0]["Hp"] <= 0:
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Hp" : 0}})

# MP -----------------------------------------------------------------------------------------
    @staticmethod
    def Change_MaxMp(DiscordID, value) : 
        Player_Data.update_one({"DiscordID" : DiscordID}, {"$inc" : {"Mana Maxima" : value}})
    
    @staticmethod
    def Change_Mp(DiscordID, value) : 
        PlayerStats =  list(Player_Data.find({"DiscordID" : DiscordID}).limit(1))

       # if the value is greater than maxium Mp, Mp goes to the maxium
        if value + PlayerStats[0]["Mp"] > PlayerStats[0]["Mana Maxima"] :
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Mp" : PlayerStats[0]["Mana Maxima"]}})

        else :
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$inc" : {"Mp" : value}})

        # Prevent from Mp be less than 0
        if value + PlayerStats[0]["Mp"] <= 0:
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Mp" : 0}})

# Corruption -----------------------------------------------------------------------------------
    @staticmethod
    def Change_Corrupt(DiscordID, value) : 
        Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Corrupcao" : value}})


# Change name ----------------------------------------------------------------------------------
    @staticmethod
    def Change_Name(DiscordID, Name) :
        if len(Name) > 2:

            # If name array is greater than 2
            # exclude word"cname" and cast the list to string
            New_Name = " ".join(Name[1::])
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Nome" : New_Name}})

        else : 
            Player_Data.update_one({"DiscordID" : DiscordID}, {"$set" : {"Nome" : Name[1]}})

# Show -----------------------------------------------------------------------------------------
    @staticmethod
    def Show_Status(DiscordID) : 
        PlayerStats =  Player_Data.find_one({"DiscordID" : DiscordID})

        return PlayerStats

    @staticmethod
    def Show_Inve(DiscordID) :
        pass
