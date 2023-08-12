
from fastapi import APIRouter, HTTPException

from models.movie import Movie

from schemas.movie import movieEntity, moviesEntity

from config.db import conn, collection, db, collection_update

from pymongo import DESCENDING, ASCENDING

from typing import List

from bson import ObjectId


movie = APIRouter()


################################################## Functions ###########################################################

def copy_collection_to_collection_update():
    # Supprimer les documents existants dans collection_update
    collection_update.delete_many({})

    # Copier tous les documents de collection vers collection_update
    collection_update.insert_many(list(collection.find()))


def update_rank():
    # Calculer et mettre à jour le nouveau 'Rank' dans collection_update en fonction du score (décroissant) et de la date de sortie (décroissante)
    ranked_movies = list(collection_update.find().sort([("Score", DESCENDING), ("Release Date", DESCENDING)]))    
    new_rank = 1
    print("Update")
    for movie in ranked_movies:
        collection_update.update_one({"_id": ObjectId(movie["_id"])}, {"$set": {"Rank": new_rank}})
        new_rank += 1



#############################################################################################################################







#########################################Query request #########################################################################

#*****************************************Tous les films **************************************************************************


@movie.get('/')
async def root():	
	return {"message": "Hello World"}



@movie.get('/list_movies')
async def find_all_movies():
    result = collection.find().sort("Rank", ASCENDING)
    movies = list(result)
    return moviesEntity(movies)


#****************************************** Listes par rangs *******************************************************************

@movie.get('/list_movies/rank/{rank}', response_model=dict)
async def list_movies_by_rank(rank: int):
    result = collection.find_one({"Rank": rank})
    return movieEntity(result)

#****************************************** Listes par annees ************************************************************

@movie.get('/list_movies/year/{year}', response_model=List[dict])
async def list_movies_by_year(year: int):
    print(f"Liste des films pour l'année {year}")
    #Trouve les films sorti au cours de l'annees "year" et tri le resusltat
    #en fontion du rang croissant
    movies = list(collection.find({"Year": year}).sort("Rank", ASCENDING))
    return moviesEntity(movies)



#****************************************** Listes par score ***********************************************************

@movie.get('/list_movies/score/{score}', response_model=List[dict])
async def list_movies_by_score(score: int):
    print(f"Liste des films pour le score : {score}")
    movies = list(collection.find({"Score": score}).sort("Rank", ASCENDING))
    return moviesEntity(movies)



#****************************************** Listes par Titres ******************************************************************

@movie.get('/list_movies/title/{title}', response_model=List[dict])
async def list_movies_by_title(title: str):
    print(f"Liste des films contenant '{title}' dans le titre")
    movies = list(collection.find({"Movie Title": {"$regex": title, "$options": "i"}}).sort("Rank", ASCENDING))
    return moviesEntity(movies)



#****************************************** Listes par Directeur ******************************************************************

@movie.get('/list_movies/director/{director}', response_model=List[dict]) 
async def list_movies_by_director(director: str):
    print(f"Liste des films realise par : '{director}' ")
    movies = list(collection.find({"Director": {"$regex": director, "$options": "i"}}).sort("Rank", ASCENDING))
    return moviesEntity(movies)



#****************************************** Listes par Cast ******************************************************************

@movie.get('/list_movies/cast/{cast}', response_model=List[dict])
async def list_movies_by_cast(cast: str):
    print(f"Liste des films ou  '{cast}' a jouer")
    movies = list(collection.find({"Cast": {"$regex": cast, "$options": "i"}}).sort("Rank", ASCENDING))
    return moviesEntity(movies)




#################################################################################################################################


##########################################Update  request #########################################################################


#***************************************** Update the score *****************************************************************

@movie.put('/update_movie_score/{rank}')
async def update_movie_score(rank: int, score: int):
    # Vérifiez si le film existe dans la collection principale
    movie = collection.find_one({"Rank": rank})
    if movie is None:
        raise HTTPException(status_code=404, detail="Film non trouvé")

    # Vérifiez si le nouveau score est inférieur ou égal à 100
    if score > 100:
        raise HTTPException(status_code=400, detail="Le nouveau score doit être inférieur ou égal à 100")

    # Mettez à jour le champ 'Score' dans collection_update
    collection_update.update_one({"Rank": rank}, {"$set": {"Score": score}})
    update_rank()

    return {"message": "Score du film mis à jour avec succès"}




#***************************************** Update the title *****************************************************************

@movie.put('/update_movie_title/{rank}')
async def update_movie_title(rank: int, movie_title: str):
    # Vérifiez si le film existe dans la collection principale
    movie = collection.find_one({"Rank": rank})
    if movie is None:
        raise HTTPException(status_code=404, detail="Film non trouvé")

    # Vérifiez si le nouveau titre est unique
    existing_movie = collection_update.find_one({"Movie Title": movie_title})
    if existing_movie:
        raise HTTPException(status_code=400, detail="Le nouveau titre existe déjà dans la base de données")

    # Mettez à jour le champ 'Movie Title' dans collection_update
    collection_update.update_one({"Rank": rank}, {"$set": {"Movie Title": movie_title}})

    return {"message": "Titre du film mis à jour avec succès"}





@movie.put('/update_all')
async def update_all():
    #Vider la collection principale
    collection.delete_many({})
    #Copier le contenu de la collection secondaire dans la collection principale
    collection.insert_many(list(collection_update.find()))

    return {"message": "Mise à jour de tous les films effectuée avec succès"}




#######################################################################################################################


##########################################Create a new User###########################################################

@movie.post('/add_movie')
async def add_movie(movie_data: Movie):
 
    # Vérifiez si le film existe déjà dans la collection_update
    existing_movie = collection_update.find_one({"Movie Title": movie_data['Movie title']})
    if existing_movie:
        raise HTTPException(status_code=400, detail="Ce film existe déjà dans la base de données")

    # Ajoutez le nouveau film à la collection_update
    collection_update.insert_one(movie_data)

    # Mettre à jour le 'Rank' dans collection_update en fonction du score (décroissant)
    update_rank()

    return {"message": "Nouveau film ajouté avec succès"}




##########################################Delete  request #########################################################################
        
    
@movie.delete('/delete_movie_by_title/{movie_title}')
async def delete_movie_by_title(movie_title: str):
    # Copier le contenu de collection vers collection_update
    copy_collection_to_collection_update()

    # Vérifiez si le film existe dans collection_update
    movie = collection_update.find_one({"Movie Title": movie_title})
    if movie is None:
        raise HTTPException(status_code=404, detail="Film non trouvé")

    # Supprimez le film de collection_update
    collection_update.delete_one({"Movie Title": movie_title})

    # Mettre à jour le 'Rank' dans collection_update en fonction du score (décroissant)
    update_rank()

    return {"message": "Film supprimé avec succès"}









