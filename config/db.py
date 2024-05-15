from pymongo import MongoClient

#Lien de connexion au Cluster
mongo_uri = ""

conn = MongoClient(mongo_uri)

db = conn["movies"] #precision du nom de la base de donnee

collection = db['netflixBestMovies'] #nom de la collection

collection_update = db["update"] #nom de la collection secondaire




