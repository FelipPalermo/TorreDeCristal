from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://FelipePalermo:ApiKey@torredecristal.zvmqwjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

inv = client["Players"].get_collection("inv")
#inv.insert_one({"Inventario" : ["item1","item2","item3"], "discordID" : "123"})

# vamos usar push como um append para listas usando update one + guildid + discordID 
inv.update_one({"discordID" : "123"}, {"$push" : {"Inventario" : {"Nome" : "Espada", "Peso" : 12, "Tipo" : "Weapon"}}})


Rinv = list(inv.find({"discordID" : "123"}))
print(Rinv[0]["Inventario"][3])


# cada item tem que ser um array 
# para poder carregar as informacoes necessarias

#Schemas 
"""
Weapon = 

    Tipo :
    Nome : 
    Dano : 
    Peso :
    Preco :

"""
