#from pymongo import MongoClient

# MongoDB connection
#mongo_uri = "mongodb+srv://pbps:h4OWt6yeN8rYLlkG@cluster0.tqxccre.mongodb.net/movies?retryWrites=true&w=majority"
#mongo_uri = "mongodb+srv://pbps:h4OWt6yeN8rYLlkG@cluster0.tqxccre.mongodb.net/?retryWrites=true&w=majority"




from pymongo import MongoClient

#Lien de connexion au Cluster
mongo_uri = "mongodb+srv://pbps:h4OWt6yeN8rYLlkG@cluster0.tqxccre.mongodb.net/?retryWrites=true&w=majority"

conn = MongoClient(mongo_uri)

db = conn["movies"] #precision du nom de la base de donnee

collection = db['netflixBestMovies'] #nom de la collection

collection_update = db["update"] #nom de la collection secondaire




