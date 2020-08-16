# FSND: Capstone Project

## Motivation for project
This is the last project of `Udacity-Full-Stack-Nanodegree` Course.
and It covers following technical topics in 1 app:
1. Database modeling with `postgres` & `sqlalchemy`
2. API to performance CRUD Operations on database with `Flask`
3. Automated testing with `Unittest`
4. Authorization & Role based Authentification with `Auth0`
5. Deployment on `Heroku`

## Start Project locally
* you need the latest version of `Python 3` and `postgres`
* Make sure you `cd` into the correct folder (with all app files) before following the setup steps.

## To start and run the local development server
* Install the dependencies:
```
$ python -m pip install -r requirements.txt
```
* edit a few informations in `config.py`, so it can
correctly connect to a local database
* Change `os.environ['DATABASE_URL']` to your local database
* If you want to test the execute tests, Run `python test_app.py`
* If you want to test the API by `postman`, you can take the existing tokens in `test_app.py`
* If you want to Run the development server `$ python app.py`

##  three types of users:
* Casting Assistant:
- Can view actors and movies

* Casting Director:
- All permissions a Casting Assistant has and
- Add or delete an actor from the database
- Modify actors or movies

* Executive Producer:
- All permissions a Casting Director has and…
- Add or delete a movie from the database

## Base URL
`https://casting-agency-api-1441.herokuapp.com/`

## Available Endpoints

|Endpoints  | Allowed Methods        |
|           |                        |
|`/actors`  | `GET POST DELETE PATCH`|
|`/movies`  | `GET POST DELETE PATCH`|

## How to work with each endpoint
    _________
** | /actors | **

1. [GET] /actors
`$ curl -X GET https://casting-agency-api-1441.herokuapp.com/actors?page1`
- Request Arguments: 
    - integer: `page` (defaults to `1` if not given)
- Requires permission: `get:actors`
- Returns: 
  1. List of dict of actors with following fields:
      - integer: `id`
      - string: `name`
      - string: `gender`
      - integer `age`
  2. boolean: `success`

* Errors
If you try fetch a page which does not have any actors, you will encounter an error:
`$ curl -X GET https://casting-agency-api-1441.herokuapp.com/actors?page5555`

will return
```py
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

2. [POST] /actors
Insert new actor into database.
`curl -X POST https://casting-agency-api-1441.herokuapp.com/actors`

- Request Arguments: none
- Request Headers: (_json_)
       1. string: `name` 
       2. integer: `age`
       3. string: `gender`
- Requires permission: `post:actors`
- Returns: 
  1. integer: `id from newly created actor`
  2. boolean: `success`

* Errors
If you try to create a new actor without a requiered field like `name`,
it will throw a `422` error:

`$ curl -X GET https://casting-agency-api-1441.herokuapp.com/actors?page55555`

will return
```py
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

3. [PATCH] /actors
Edit an existing Actor
`$ curl -X PATCH https://casting-agency-api-1441.herokuapp.com/actors/1`

- Request Arguments: integer: `actor id`
- Request Headers: (_json_)
       1. string: `name` 
       2. integer: `age` 
       3. string: `gender`
- Requires permission: `edit:actors`
- Returns: 
  1. integer: `id from updated actor`
  2. boolean: `success`
  3. List of dict of actors

* Errors
If you try to update an actor with an invalid id it will throw an `404`error:

`$ curl -X PATCH https://casting-agency-api-1441.herokuapp.com/actors/55555`
will return

```py
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

4. [DELETE] /actors
Delete an existing Actor
`$ curl -X DELETE https://casting-agency-api-1441.herokuapp.com/actors/1`
- Request Arguments: integer: `actor id`
- Request Headers: `None`
- Requires permission: `delete:actors`
- Returns: 
  1. integer: `id from deleted actor`
  2. boolean: `success`

* Errors
If you try to delete actor with an invalid id, it will throw an `404`error:

`$ curl -X DELETE https://casting-agency-api-1441.herokuapp.com/actors/5555`
will return

```py
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```
    _________
** | /movies | **

1. [GET] /movies
`$ curl -X GET https://casting-agency-api-1441.herokuapp.com/movies?page1`
- Request Arguments: 
    - integer `page` (`1` if not given)
- Request Headers: **None**
- Requires permission: `get:movies`
- Returns: 
  1. List of dict of movies with following fields:
      - integer `id`
      - string `name`
      - date `release_date`
  2. boolean `success`

* Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:
`$ curl -X GET https://casting-agency-api-1441.herokuapp.com/movies?page55555`
will return

```py
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

2. [POST] /movies
Insert new Movie into database.
`$ curl -X POST https://casting-agency-api-1441.herokuapp.com/movies`
- Request Arguments: **None**
- Request Headers: (_json_)
       1. string: `title` 
       2. date: `release_date` 
- Requires permission: `post:movies`
- Returns: 
  1. integer: `movie id`
  2. boolean: `success`

* Errors
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

`$ curl -X GET https://casting-agency-api-1441.herokuapp.com/movies?page5555`
will return

```py
{
  "error": 422,
  "message": "unprocessable",
  "success": false
}
```

3. [PATCH] /movies
Edit an existing Movie
`$ curl -X PATCH https://casting-agency-api-1441.herokuapp.com/movies/1`
- Request Arguments: integer: `movie id`
- Request Headers: (json)
       1. string: `title` 
       2. date: `release_date` 
- Requires permission: `edit:movies`
- Returns: 
  1. integer: `id from updated movie`
  2. boolean: `success`
  3. List of dict of movies 

* Errors
If you try to update an movie with an invalid id it will throw an `404`error:

`$ curl -X PATCH https://casting-agency-api-1441.herokuapp.com/movies/5555`
will return

```py
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

4. [DELETE] /movies
Delete an existing movie
`$ curl -X DELETE https://casting-agency-api-1441.herokuapp.com/movies/1`
- Request Arguments: integer: `movie id`
- Request Headers: `None`
- Requires permission: `delete:movies`
- Returns: 
  1. integer: `movie id`
  2. boolean: `success`

* Errors
If you try to delete movie with an invalid id, it will throw an `404`error:
`$ curl -X DELETE https://casting-agency-api-1441.herokuapp.com/movies/5555`
will return

```py
{
  "error": 404,
  "message": "resource not found",
  "success": false
}
```

## Authentification

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name and select "Regular Web Application"
5. Go to Settings and find `domain`. Copy & paste it into models.py
6. Click on API Tab 
7. Create a new API:
8. Go to Settings and find `Identifier`. Copy & paste it into auth.py

#### Create Roles & Permissions
1. Before creating 'Roles & Permissions', you need to 'Enable RBAC' in your API 
2. check the button 'Add Permissions in the Access Token'.
3. create a new Role under 'Users and Roles' => 'Roles' => 'Create Roles'
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions 
6. After you created all permissions , go back to 'Users and Roles' => 'Roles' and select the role.
7. Under 'Permissions', assign all permissions you want this role to have. 

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (get:actors): Can see all actors
  - GET /movies (get:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (post:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (post:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database