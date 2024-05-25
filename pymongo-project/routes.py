from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List 

from models import Movie, MovieUpdate, PersonMovieReview

router = APIRouter() 

# QUESTION 1 - return all movies 
@router.get("/", response_description="List all Movies", response_model=List[Movie])
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find(limit=1))
    return movies 


# QUESTION 2
@router.get("/{movie}", response_description="Get a movie by title or actor's name", response_model=List[Movie])
def find_movie(parameter: str, request: Request):
    movies_by_title = list(request.app.database["movies"].find({"title": parameter}))
    movies_by_actor = list(request.app.database["movies"].find({"actors": parameter}))

    for movie in movies_by_title + movies_by_actor: 
        movie["_id"] = str(movie["_id"])

    if movies_by_title:
        return jsonable_encoder(movies_by_title)
    elif movies_by_actor:
        return jsonable_encoder(movies_by_actor)

    raise HTTPException(status_code=404, detail=f"No movies found with parameter '{parameter}'")

# QUESTION 3
@router.put("/{title}", response_description="Update a movie by title", response_model=Movie)
def update_movie_by_title(title: str, request: Request, movie_update: MovieUpdate):
    movie = request.app.database["movies"].find_one({"title": title})
    
    if not movie:
        raise HTTPException(status_code=404, detail=f"No movie found with title '{title}'")
    
    movie_data = movie_update.dict(exclude_unset=True)
    updated_movie = request.app.database["movies"].find_one_and_update(
        {"title": title}, 
        {"$set": jsonable_encoder(movie_data)}, 
        return_document=True
    )
    
    updated_movie["_id"] = str(updated_movie["_id"])

    return updated_movie 



@router.get("/neo4j-mongodb/movies", response_description="Get movies in common between MongoDB & Neo4j", response_model=str)
def get_neo4j_movies(request: Request):
    # Récupérer les titres des films depuis Neo4j
    neo4j_movie_docs = request.app.neo4j_client.get_movie_documents()
    neo4j_movie_titles = [doc['properties']['title'] for doc in neo4j_movie_docs]

    # Rechercher les films correspondants dans MongoDB
    movies_mongodb = []
    for title in neo4j_movie_titles:
        movie = request.app.database["movies"].find_one({"title": title})
        if movie:
            # Supprimer le champ '_id' du document MongoDB
            del movie['_id']
            movies_mongodb.append(Movie(**movie))
    num_common_movies = len(movies_mongodb)

    return f"Neo4j et MongoDB ont {num_common_movies} films en commun" 




@router.get("/neo4j-users-reviewed/{user}", response_description="Get Users who reviewed a film given in parameter", response_model=PersonMovieReview)
def get_neo4j_users_rated_movie(request: Request, user: str):
    # Définir la requête Cypher pour récupérer les utilisateurs qui ont revu un film donné
    cypher_query = f"""
    MATCH 
        (p:Person {{name: '{user}'}})-[:REVIEWED]->(m:Movie)
    RETURN 
        p.name,
        count(m) as nbMoviesRated, 
        collect(m.title) as moviesRated
    """

    # Exécuter la requête Cypher
    result = request.app.neo4j_client.run_cypher_query(cypher_query)

    # Récupérer tous les enregistrements du résultat
    records = list(result)

    # S'il n'y a pas d'enregistrement, renvoyer un dictionnaire vide
    if not records:
        return {}

    # Récupérer le premier enregistrement
    record = records[0]

    # Créer une instance de PersonMovieReview à partir de l'enregistrement
    person_review = PersonMovieReview(
        name=record["p.name"],
        nbMovies=record["nbMoviesRated"],
        moviesRated=record["moviesRated"]
    )

    return person_review


