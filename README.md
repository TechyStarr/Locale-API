# Locale-API

Locale is a developer tool for anyone who needs to know Nigeria, geographically at least. Locale's API shows you all of Nigeria's regions, 
states, and local government areas (LGAs). Locale is looking to be a very useful tool for the thousands of businesses building for Nigeria's 200M+ population size.


Locale was built using Python

## Table of Contents

- [Locale](#Locale)
  - [Table of Contents](#table-of-contents)
  - [Live ( deployed version )](#live--deployed-version-)
  - [Implementations](#implementations)
  - [Technologies Used](#technologies-used)
  - [Libraries Used](#libraries-used)
  - [Usage ( deployed version )](#usage--deployed-version-)
  - [Testing Locally](#testing-locally)
  - [Available Endpoints](#available-endpoints)
     - [Authorization Endpoints](#authorization-endpoints)
     - [Testing View Endpoints](#view-endpoints)
     -  [Search Endpoints Locally](#search-endpoints)
     - [User Endpoints](#user-endpoints)
    
  

## Live ( deployed version )
### [Website](https://locale-lkbw.onrender.com)

## Implementations
1. Search functions
2. Data Filtering

## Technologies Used

- Python
- Flask
- PostgreSQL

<p align="right"><a href="#readme-top">back to top</a></p>

## Libraries Used
- [Flask restx](https://flask-restx.readthedocs.io/en/latest/) - a framework for creating REST API
- [Flask migrate](https://flask-migrate.readthedocs.io/) - a framework for tracking database modifications
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - object-relational mapper
- [Flask JWT extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - authentication and authorization
- [Flask Mail](https://pythonhosted.org/Flask-Mail/) - sending emails
- [Flask Caching](https://flask-caching.readthedocs.io/en/latest/) - Database Cache layering
- [Flask Limiter](https://flask-limiter.readthedocs.io/en/stable/) - Rate limiting
- [Flask CORS](https://flask-cors.readthedocs.io/en/latest/) - Handle Cross-Origin Resource Sharing
<p align="right"><a href="#readme-top">back to top</a></p>
  
### Usage (deployed version)
1. Visit [website](https://locale-lkbw.onrender.com) on your web browser


2. Create an account as an admin
    - Click "Auth" to reveal the authentication endpoints
    - Register with your preferred details


3. Sign in to your account
    - Input the details you registered with to generate a JWT token
    - Copy this access token without the quotation marks


4. Click on the "Authorize" button at the top right. Enter the JWT token prefixed with "Bearer" in the given format
    ```
    Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlIj
    ```
    
5. Click "Authorize", then close the pop-up


6. Now authorized, you can use the endpoints by creating, viewing, updating and deleting both students and courses.


7. Click the 'Authorize' button, then logout to logout


## Testing Locally

Clone the repository


```console
git clone https://github.com/TechyStarr/Student-Management-API.git
```



Navigate into the project folder

```console
cd student-mgt
```

Create a virtual environment

``` console
py -3 -m venv env
```

Activate the virtual environment

Windows: ``` console env/scripts/activate ```
Linux or Mac: source env/bin/activate

Install the necessary dependencies to run the project

```console
pip install -r requirements.txt
```

Create a FLASK_APP environment variable

``` console
export FLASK_APP=runserver.py
```


Run application

```console
flask run
```

or

```console
py runserver.py
```
<p align="right"><a href="#readme-top">back to top</a></p>




## Available Endpoints

### Authorization Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/auth/signup` | _POST_ | It allows an admin to create an account  | Any | Any |  ---- | 
|  `/auth/login` |  _POST_  | Generates an access and refresh token for user authentication | Any | Any | ---- | 
|  `/auth/logout` |  _POST_  | It is used to logout user and blacklist token   | Authenticated | Any | ---- | 
|  `/auth/refresh` |  _POST_  | It is used to refresh expired tokens   | Authenticated | Any | ---- | 
|  `/auth/validate_token` |  GET  | It is used to validate JWT tokens   | Authenticated | Any | ---- | 
|  `/auth/generate-api-key` |  _POST_  | It is used to generate API Key   | Authenticated | Any | ---- | 
|  `/auth/apikeys` |  GET  | It is used to retrieve all API keys for a user  | Authenticated | Any | ---- | 



### View Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/view/regions` |  _GET_  | Retrieve all regions   | Authenticated | Any | ---- |
|  `/view/states` |  _GET_  | Retrieve all states   | Authenticated | Any | ---- |
|  `/view/lgas` |  _GET_  | Retrieve all lgas   | Authenticated | Any | ---- |
|  `/view/regions/<region_id/states>` |  _GET_  | Retrieve all states under a region by ID | Authenticated | Any | region ID |
|  `/view/state/<state_id>` |  _GET_  | Retrieve all states by ID | Authenticated | Any | state ID |
|  `/view/lga/<lga_id>` |  _GET_  | Retrieve all lgas by ID | Authenticated | Any | lga ID |
|  `/view/places` |  _GET_  | Retrieve all places of interest   | Authenticated | Any | ---- |
|  `/view/place/state/<state_id>` |  _GET_  | Retrieve all places of interest in a state | Authenticated | Any | ---- |
|  `/view/load-dataset` |  _POSTT_  | Manually load dataset   | Authenticated | Any | ---- |
|  `/view/regions` |  _GET_  | Read dataset   | Authenticated | Any | ---- |



### Search Endpoints
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `/query` |  _GET_  | Search for states, regions and local government areas  | Authenticated | Any |
|  `/filter` |  _GET_  | Filter by either region, states or lga   | Authenticated | Any | state ID |
|  `/query/place/state/<state_id>` |  _GET_  | Retrieve all places of interest in a state | Authenticated | Any | ---- |


