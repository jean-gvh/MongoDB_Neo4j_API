from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from neo4j import GraphDatabase
from routes import router as movie_router

config = dotenv_values(".env")

app = FastAPI()

# MongoDB connection
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# Neo4j connection
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_movie_documents(self):
        with self.driver.session() as session:
            result = session.run("MATCH (m:Movie) RETURN m")
            return [
                {
                    "identity": record["m"].id,
                    "labels": list(record["m"].labels),
                    "properties": dict(record["m"]),
                    "elementId": record["m"].element_id
                }
                for record in result
            ]
        
    def run_cypher_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            records = list(result)  # Récupérer tous les enregistrements
            return records


@app.on_event("startup")
def startup_neo4j_client():
    app.neo4j_client = Neo4jConnection(config["NEO4J_URI"], config["NEO4J_USER"], config["NEO4J_PASSWORD"])

@app.on_event("shutdown")
def shutdown_neo4j_client():
    app.neo4j_client.close()

# Include the routes from routes.py
app.include_router(movie_router, tags=["movies"], prefix="/movie")
