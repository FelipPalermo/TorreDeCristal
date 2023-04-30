from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://FelipePalermo:ApiKey@torredecristal.zvmqwjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

Player_Data = client["Players"].get_collection("Player_Data")

# Classe Personagem ----------------------------------------

class Player :

    def __init__(self, Nome, VidaMaxima, Vida, ManaMaxima, Mana, Corrupcao) :

        self.Nome = Nome 
        self.Vida_Maxima = VidaMaxima
        self.Hp = Vida
        self.Mana_Maxima = ManaMaxima
        self.Mana = Mana
        self.Corrupcao = Corrupcao
        self.PlayerStats = list(Player_Data.find({"Nome" : self.Nome}).limit(1)) 
 
        if Player_Data.count_documents({"Nome" : self.Nome}) >= 1 :
            pass

        else :
            Player_Data.insert_one({
                "Nome" : self.Nome,
                "Vida Maxima" : self.Vida_Maxima,
                "Hp" : self.Hp,
                "Mana Maxima" : self.Mana_Maxima,
                "Mp" : self.Mana, 
                "Corrupcao" : self.Corrupcao})
    
    def DelChar(self) : 
        filtro = {"Nome" : self.Nome}
        Player_Data.delete_one(filtro)
     
# HP -----------------------------------------------------------------------------------------

    def Change_MaxHp(self, value) : 
        Player_Data.update_one({"Nome" : self.Nome}, {"$inc" : {"Vida Maxima" : value}})

    def Change_Hp(self, value) :
        # Retorna documento para variavel
        #PlayerStats = list(Player_Data.find({"Nome" : self.Nome}).limit(1)) 

       # Se o valor indicado for maior que a vida maxima, a vida vai para o maixmo possivel
        if value + self.PlayerStats[0]["Hp"] > self.PlayerStats[0]["Vida Maxima"] :
            Player_Data.update_one({"Nome" : self.Nome}, {"$set" : {"Hp" : self.PlayerStats[0]["Vida Maxima"]}})
         
        else :
            Player_Data.update_one({"Nome" : self.Nome}, {"$inc" : {"Hp" : value}})
       
        # Impede de ficar com valores menores que 0 de HP
        if value + self.PlayerStats[0]["Hp"] <= 0:
            Player_Data.update_one({"Nome" : self.Nome}, {"$set" : {"Hp" : 0}})

# MP -----------------------------------------------------------------------------------------

    def Change_MaxMp(self, value) : 
        Player_Data.update_one({"Nome" : self.Nome}, {"$inc" : {"Mana Maxima" : value}})

    def Change_Mp(self, value) :
        #PlayerStats = list(Player_Data.find({"Nome" : self.Nome}).limit(1)) 

       # Se o valor indicado for maior que o MP maximo, o MP vai para o maixmo possivel
        if value + self.PlayerStats[0]["Mp"] > self.PlayerStats[0]["Mana Maxima"] :
            Player_Data.update_one({"Nome" : self.Nome}, {"$set" : {"Mp" : self.PlayerStats[0]["Mana Maxima"]}})

        else :
            Player_Data.update_one({"Nome" : self.Nome}, {"$inc" : {"Mp" : value}})
       
        # Impede de ficar com valores menores que 0 de MP
        if value + self.PlayerStats[0]["Mp"] <= 0:
            Player_Data.update_one({"Nome" : self.Nome}, {"$set" : {"Mp" : 0}})

# Corrupcao -----------------------------------------------------------------------------------

    def Change_Corrupt(self, value) : 
        Player_Data.update_one({"Nome" : self.Nome}, {"$set" : {"Corrupcao" : value}})


