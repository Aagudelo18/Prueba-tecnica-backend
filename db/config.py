from pymongo import MongoClient

uri = "mongodb+srv://alejandraagudelocartagena:alejandra18@cluster0.uidg5gp.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client.gestion_logistica
