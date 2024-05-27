# Final Lab Neo4j x MongoDB 


Requirements :
1. You need to install MongoDB database tools
1. You need a MongoDB account to run Atlas (free tier) | https://www.mongodb.com/fr-fr
2. You need to download Neo4j Desktop and follow the instructions to set up the database server.
3. You need Python and an IDE such as vscode for example.


# Step-by-Step Guide


### Setup the Repository
Create a folder on your local machine, then cd in that folder and run this command in your terminal : 
``` bash
git clone https://github.com/jean-gvh/final-lab.git
```

### Set up the MongoDb Database
Once you have created your account, created your project and choosen the freetier option for your atlas cluster, do these steps in order have the right set up.
Use the mongoimport CLI tool to import the Movie JSON document in the repo. with the following command.


mongoimport --uri 
mongodb+srv://<USERNAME>:<PASSWORD>@<CLUSTER_NAME>/<DATABASE> --collection <COLLECTION> --type json --file /your-project-dirctory/Movies.json 


### Set up the Python environment
Prerequites :
Edit the .env file with your own credential in order to run successfully the app.
1. cd into your project location and then run this command to create a virtual environement :
``` bash 
python -m venv env_name
```
2. Activate the venv by cd into the env_name folder and then run : .\Scripts\Activate.ps1
3. Install all the necessary :
```bash
pip install requirements.txt
```
At this point you should have : a venv activated with all python packages installed in it.

4. cd into the main project location.
5. run the gunicorn server by running :  
``` bash 
python -m uvicorn main:app --reload
```
6. go to your brower and copy this into it : localhost:8000/docs. You should see a page with all the routes set up


#GG you can now interact with the API's and test the routes !
   






