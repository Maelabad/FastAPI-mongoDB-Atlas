
from fastapi import FastAPI

from routes.movie import movie # Importation des routes spécifiques

# Création de l'instance de l'application FastAPI
app = FastAPI()

# Inclusion des routes dans l'application
app.include_router(movie)



