# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
'''https://shaf3y.us.auth0.com/authorize?audience=udacity-cafe&response_type=token&client_id=p5w4QFxPPnLyT6tkpsynim2ApwQEWDuk&redirect_uri=http://127.0.0.1:8080/login-result''''

barista----

'''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpaYUdHWWVjWFRUbjlBck1OZFcyYiJ9.eyJpc3MiOiJodHRwczovL3NoYWYzeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmOGUxYjE2NTJlNWEwMDE5Y2UwNzVlIiwiYXVkIjoidWRhY2l0eS1jYWZlIiwiaWF0IjoxNTkzMzY5MzMzLCJleHAiOjE1OTMzNzY1MzMsImF6cCI6InA1dzRRRnhQUG5MeVQ2dGtwc3luaW0yQXB3UUVXRHVrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.N7oWAChq9wKn77IC0-nO1UirZqjKD2FBDbP78hZPW8U2DZQCuRPthX_KLlPVSzM5QpBonTqQedmURNIJIxCq2kyztHEk1gpZseGOqshqyLPxwhAICkZFIN2gT2wxUn0KCjPOLdgR4uVzHQLbJVPma0h55LCedOQqZNEvUtUGZlBQDQLgq8wEVZpffsiW6-6UoSCQNMrcpb6ooa4V5mb3wlFndTxj0lFnDRRE_Xrk1IwWQiJMwKXaUS3Xjq8gc-k0f8fDMxZ3U0hRmCLkFID0pi2JIbBJ4eq9rLjvdG1gtmuIJ2jmmgjDPMbiYRVJLn9tRg-jPYlC_HgbyZhkDGoNVQ'''


manager----

''''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlpaYUdHWWVjWFRUbjlBck1OZFcyYiJ9.eyJpc3MiOiJodHRwczovL3NoYWYzeS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmOGUyOTA2NTJlNWEwMDE5Y2UwNzZkIiwiYXVkIjoidWRhY2l0eS1jYWZlIiwiaWF0IjoxNTkzMzc0NjExLCJleHAiOjE1OTMzODE4MTEsImF6cCI6InA1dzRRRnhQUG5MeVQ2dGtwc3luaW0yQXB3UUVXRHVrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.jnJd_Fe8hfqN6GP9yRiApOR4HXv74-i4eea5nKwoW673a4Wwq7km3jt_xMoq3CkVcHry-uvxghJHdU-XUT9DHElo4VD90uRo5bkNhBsxGFTHyJtIuhrFskGfSzKd4M9eQwmSSu_30I-BgrLChxzFhtJcm96xtDNqrCBCo2d4E-sJNN3Yy9LSCl_Yhkp44Z7DBUs3_czBmfNK5uSZXSugHQ-CxnBQq1ED57jt_OKjy-TIHp-bzLS-Euvk2GBDJ9aTQ5mq2QtCKB4PelseAJbwwx-ynIYDDDznCZQEJZfnBy_DOQvUkohxlV9kGq4U11kdVbHhXePIu1ez3oSJfLVJ-g''''