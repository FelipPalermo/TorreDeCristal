from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://FelipePalermo:ApiKey@torredecristal.zvmqwjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

class Server : 
    
    def __init__(self, atr) :
        
        self.leanguage = atr[0].lower()
        self.GuildID = atr[1]
        
        if client[str(self.GuildID)].Server.count_documents({"GuildID" : self.GuildID}) :
            pass

        else :
           
            client[str(self.GuildID)].Server.insert_one({
                "GuildID" : str(self.GuildID),
                "Leanguage" : self.leanguage,
                "AntiFlood" :  True
})


# Change Anti flood parameter in MongoDB ---------------------------------------------------------------------
    @staticmethod
    def AntiFlood(GuildID) :
        
        if list(client[str(GuildID)].Server.find({"GuildID" : str(GuildID)}).limit(1))[0]["AntiFlood"] == True :

            client[str(GuildID)].Server.update_one({"GuildID" : str(GuildID)},{"$set" : {"AntiFlood" : False }})

        else : 

            client[str(GuildID)].Server.update_one({"GuildID" : str(GuildID)},{"$set" : {"AntiFlood" : True }})

# Return True and False for comparations -------------------------------------------------------------------- 
    @staticmethod
    def RAntiFlood(GuildID) :  
        if list(client[str(GuildID)].Server.find({"GuildID" : str(GuildID)}).limit(1))[0]["AntiFlood"] == True :

            return True

        else :
            return False
