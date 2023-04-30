from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://FelipePalermo:ApiKey@torredecristal.zvmqwjj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

Player_Data = client["Players"].get_collection("Player_Data")

a = list(Player_Data.find({"Nome" : "Nico cat"}).limit(1))

print(a[0]["Hp"])
