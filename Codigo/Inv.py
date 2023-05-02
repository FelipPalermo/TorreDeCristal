from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://FelipePalermo:ApiKey@torredecristal.zvmqwjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

Player_Inv = client["Players_Inv"].get_collection("Inventario")

class Inventario : 
    
    def __init__(self, Nome, DiscordId) :

        self.DiscordId = DiscordId
        self.Nome = Nome.lower()
        self.InvStatus = list(Player_Inv.find({"Nome" : self.Nome}).limit(1))
        
        if Player_Inv.count_documents({"Nome" : self.Nome}) >= 1:
            pass

        else :
            Player_Inv.insert_one({
                "DiscordId" : self.DiscordId,
                "Nome" : self.Nome,  
                "Fragmentos de cristal" : 0,
                "Inventario" : [] })


    def Add_Inv(self, *itens) : 

        
        if itens == None :
            pass
        else :
            for i in itens :
                    Player_Inv.update_one({"Nome" : self.Nome}, {"$push" : {"Inventario" : i}})

    def Show_Inv(self) : 

        result = Player_Inv.find({"Nome" : self.Nome})
        for i in result :
            print(i["Inventario"])

inv = Inventario("felipe", "3")
inv.Add_Inv(["almondega", "rubuga"])
inv.Show_Inv()
