# Backup Baristas API

## The problem
Finding emergency backup staff to cover shift vacancies due to sickness and emergency commitments is one of the many problems that is always faced by many hospitality businesses especially among cafés and restaurants. The situation has gotten after covid-19 pandemic due to lockdowns which force many skilled employee of hospitality leaving the industry. 

## The purpose of this API
* Help cafés find skilled workers to cover emergency shift vacancy
* Help skilled workers(baristas) to earn some extra income

## Database system
The chosen DBMS for this API is PostgreSQL. 
### Why PostgreSQL?
* PostgreSQL supports all needed datatypes and structures
* It provides data integrity by using constraints and regulate all datas which will be stored in the database
* High performance when read and create new record of data

### Drawbacks of PostgreSQL
* Unlike file based DBMS such as MongoDB, all records has to follow schemas defined by models
* Relatively slower access speed compare to some other DBMS

## Key functionality and benefits of ORM
Object-relational mapper or ORM creates an abstract oop layer between the database and the programming language we are using. When we query the database, instead writing the more complex SQL we can write queried in the way of object-oriented paradigm which we are familiar with in the programming language we chose. This will speed up the development time of a project.

## ERD
![ERD](docs/backup_barista_api.jpeg)

## Relations
**Venues** - id(PK), venue_name, address, city, email, abn, phone, manager_id(FK)<br>
**Managers** - id(PK), username, password, first_name, last_name, email, contact_number, date_joined<br>
**Baristas** - id(PK), username, password, first_name, last_name, email, address, contact_number, join_date, rating<br>
**Jobs** - id(PK), description, date, start_time, finish_time, rate, status, barista_id(FK), venue_id(FK)<br>
**Applications** - id(PK), job_id(FK), barista_id(FK), status<br>
**Reviews** - id(PK), comments, rating, barista_id(FK), job_id(FK)

## Relationships between models
1. Each manager can manage zero or more venues
2. Each venue can have zero or more job posted
3. Each barista can submit zero or more applications
4. Each barista can be reviewed zero or more times
5. Each job can only be reviewed zero or one time
6. Each job can only be assigned with zero or one barista
7. Each job can have zero or more applications from different baristas

## Database relations and functions to be implemented in this API

1. Users of the API are able to register as managers or baristas
2. Managers and baristas are able to login and bearer token will be returned to users, bearer token will be later used to identify and authenticate user to allow API operations
3. After login, managers are able to create new venues and post new jobs on behalf of venues that they manages
4. Managers are able to update venue details or delete venues if they no longer manage that venue
5. Managers are able to update/delete jobs they posted
6. After login, baristas are able to apply for jobs and applications will be stored in the applications table
7. Baristas are able to withdraw/delete their application if the status is still pending
8. Managers are able to view all applications. if there is suitable barista for the job, the manager can approve that application and all rest applications for the job will be marked as unsuccessful
9. After the job has been fulfilled, managers are able to leave a rating and comments to how the barista has performed

## Dependencies which required to run this API
```
bcrypt==3.2.2
cffi==1.15.1
click==8.1.3
Flask==2.2.2
Flask-Bcrypt==1.0.1
Flask-JWT-Extended==4.4.4
flask-marshmallow==0.14.0
Flask-SQLAlchemy==2.5.1
importlib-metadata==4.12.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
marshmallow==3.17.0
marshmallow-sqlalchemy==0.28.1
packaging==21.3
psycopg2==2.9.3
pycparser==2.21
PyJWT==2.4.0
pyparsing==3.0.9
python-dotenv==0.20.0
six==1.16.0
SQLAlchemy==1.4.40
Werkzeug==2.2.2
zipp==3.8.1
```

## 3rd party services that this API will use in the future
The API is currently still in development with all routes are connect to a local server. Upon completion, this API will be hosted on [heroku](https://www.heroku.com/) server.

## API documentations

<span style="color:green;">**GET**</span> - Get all jobs
```
[GET]http://127.0.0.1:5000/jobs
```
Get all available jobs which still need to be fulfilled.<br>
*Example output:*
```json
[
    {
        "id": 1,
        "description": "Barista required for busy cafe on Sunday",
        "date": "2022-09-22",
        "start_time": "10:00:00",
        "finish_time": "14:00:00",
        "pay_rate": 35,
        "status": "To be fulfilled",
        "barista": null,
        "venue": {
            "id": 1,
            "venue_name": "cafe1",
            "address": "12 Connell Way Belconnen ACT 2617",
            "city": "Canberra",
            "email": "info@cafe1.com",
            "abn": "180180180",
            "contact_number": "0261235678"
        }
    },
    {
        "id": 2,
        "description": "Barista wanted Saturday",
        "date": "2022-09-25",
        "start_time": "08:00:00",
        "finish_time": "16:00:00",
        "pay_rate": 35,
        "status": "To be fulfilled",
        "barista": null,
        "venue": {
            "id": 2,
            "venue_name": "cafe2",
            "address": "112 George St Sydney NSW 2000",
            "city": "Sydney",
            "email": "info@cafe2.com",
            "abn": "191191191",
            "contact_number": "0298765432"
        }
    }
]
```

<span style="color:green;">**GET**</span> - Get all jobs matching searching criteria<br><br>
**Query Params**
- min_rate[optional]
- location[optional]
```
[GET]http://127.0.0.1:5000/jobs?min_rate[optional]=30&location[optional]=canberra
```
Get all available jobs which still need to be fulfilled with matching criteria.<br>
*Example output:*
```json
[
    {
        "id": 1,
        "description": "Barista required for busy cafe on Sunday",
        "date": "2022-09-22",
        "start_time": "10:00:00",
        "finish_time": "14:00:00",
        "pay_rate": 35,
        "status": "To be fulfilled",
        "barista": null,
        "venue": {
            "id": 1,
            "venue_name": "cafe1",
            "address": "12 Connell Way Belconnen ACT 2617",
            "city": "Canberra",
            "email": "info@cafe1.com",
            "abn": "180180180",
            "contact_number": "0261235678"
        }
    }
]
```
<span style="color:orange;">**POST**</span> - Manager register
```
[POST]http://127.0.0.1:5000/auth/manager/register
```
Description: Register managers and return authentication bearer token.<br><br>
**Request Body** (json)
```json
{
    "username":"manager3",
    "password":"********",
    "first_name":"James",
    "last_name":"Kelly",
    "email":"james@email.com",
    "contact_number":"0455661123"
}
```
*Example output:*
```json
{
    "username": "manager3",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NDY3NjEyOSwianRpIjoiZDNhY2IxNGUtMDM1My00MjA5LTg3NDItZmIxNzg4M2ZlYTkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hbmFnZXIzIiwibmJmIjoxNjY0Njc2MTI5LCJleHAiOjE2NjQ3NjI1Mjl9._TBIaHq9qjFQO_JewwwDdCBFwzThJMcFAushsqklr8"
}
```

<span style="color:orange;">**POST**</span> - Create new venue
```
[POST]http://127.0.0.1:5000/venues
```
Description: Create new venue managed by current signed in manager.<br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
**Request Body** (json)
```json
{
    "venue_name":"Cool cafe",
    "address":"101 Rock st Canberra 2612",
    "email":"info@coolcafe.com",
    "abn":"123456789",
    "contact_number":"0288888888"
}
```
*Example output:*
```json
{
    "id": 5,
    "venue_name": "Cool cafe",
    "address": "101 Rock st Canberra 2612",
    "city": "canberra",
    "email": "info@coolcafe.com",
    "abn": "123456789",
    "contact_number": "0288888888",
    "manager": {
        "id": 3,
        "first_name": "James",
        "last_name": "Kelly",
        "email": "james@email.com",
        "contact_number": "0455661123"
    },
    "jobs": []
}
```

<span style="color:orange;">**POST**</span> - Create new job
```
[POST]http://127.0.0.1:5000/jobs/<venue_id>
```
Description: Create new job for venue with associate venue_id<br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
**Request Body** (json)
```json
{
    "description":"Super star worker needed!",
    "date":"2022-9-30",
    "start_time":"8:00",
    "finish_time":"15:00",
    "pay_rate":40
}
```
*Example request:*
```
[POST]http://127.0.0.1:5000/jobs/2
```
*Example output:*
```json
{
    "id": 3,
    "description": "Super star worker needed!",
    "date": "2022-09-30",
    "start_time": "08:00:00",
    "finish_time": "15:00:00",
    "pay_rate": 40,
    "status": "To be fulfilled",
    "barista": null,
    "venue": {
        "id": 2,
        "venue_name": "cafe2",
        "address": "112 George St Sydney NSW 2000",
        "city": "Sydney",
        "email": "info@cafe2.com",
        "abn": "191191191",
        "contact_number": "0298765432"
    }
}
```

<span style="color:orange;">**POST**</span> - Manager login
```
[POST]http://127.0.0.1:5000/auth/manager/login
```
Description: Manager login and bearer token will be returned for later perform API operation.<br>

**Request Body** (json)
```json
{
    "username":"manager2",
    "password":"12345678"
}
```
*Example output:*
```json
{
    "username": "manager2",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NDY3Nzk2NiwianRpIjoiNmMyZDMwY2EtZWU3OC00MWQzLWJmYjItNzA2M2E3OTMxMTgwIiwHlwZSI6ImFjY2VzcyIsInN1YiI6Im1hbmFnZXIyIiwibmJmIjoxNjY0Njc3OTY2LCJleHAiOjE2NjQ3NjQzNjZ9.9suHx7Vmzm55gGgtygrOOTMsTjGsHCFY27QyXBjdcTA"
}
```
<span style="color:blue;">**PUT**</span> - Update job details
```
[PUT]http://127.0.0.1:5000/jobs/<job_id>
```
Description: Update job details with associate venue_id, user may update certain fields of the job and leave other fields unchanged. <br><br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
**Request Body** (json)
```json
{
    "description":"Helper barista needed!",
    "pay_rate":50
}
```
*Example request:*
```
[PUT]http://127.0.0.1:5000/jobs/3
```
*Example output:*
```json
{
    "id": 3,
    "description": "Helper barista needed!",
    "date": "2022-09-30",
    "start_time": "08:00:00",
    "finish_time": "15:00:00",
    "pay_rate": 50,
    "status": "To be fulfilled",
    "barista": null,
    "venue": {
        "id": 2,
        "venue_name": "cafe2",
        "address": "112 George St Sydney NSW 2000",
        "city": "Sydney",
        "email": "info@cafe2.com",
        "abn": "191191191",
        "contact_number": "0298765432"
    }
}
```

<span style="color:green;">**GET**</span> - Get all jobs of a venue
```
http://127.0.0.1:5000/jobs/<venue_id>
```
Description: Get all available jobs which associated with a venue<br><br>
*Example request*
```
[GET]http://127.0.0.1:5000/jobs/2
```
*Example output:*
```json
[
    {
        "id": 2,
        "description": "Barista wanted Saturday",
        "date": "2022-09-25",
        "start_time": "08:00:00",
        "finish_time": "16:00:00",
        "pay_rate": 35,
        "status": "To be fulfilled",
        "barista": null,
        "venue": {
            "id": 2,
            "venue_name": "cafe2",
            "address": "112 George St Sydney NSW 2000",
            "city": "Sydney",
            "email": "info@cafe2.com",
            "abn": "191191191",
            "contact_number": "0298765432"
        }
    },
    {
        "id": 3,
        "description": "Helper barista needed!",
        "date": "2022-09-30",
        "start_time": "08:00:00",
        "finish_time": "15:00:00",
        "pay_rate": 50,
        "status": "To be fulfilled",
        "barista": null,
        "venue": {
            "id": 2,
            "venue_name": "cafe2",
            "address": "112 George St Sydney NSW 2000",
            "city": "Sydney",
            "email": "info@cafe2.com",
            "abn": "191191191",
            "contact_number": "0298765432"
        }
    }
]
```

<span style="color:orange;">**POST**</span> - Barista login
```
[POST]http://127.0.0.1:5000/auth/login
```
Description: Barista login and bearer token will be returned for later perform API operation.<br>

**Request Body** (json)
```json
{
    "username":"barista1",
    "password":"*********"
}
```
*Example output:*
```json
{
    "username": "barista1",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NDY4NDg2OCwianRpIjoiMTMxNTI3MzgtODAwOC00ZTZlLWJlYTEtMWM4OWVjMWM0MmQ5IiwidHlwZSI6ImFjY2VzcyIN1YiI6InVzZXIxIiwibmJmIjoxNjY0Njg0ODY4LCJleHAiOjE2NjQ3NzEyNjh9.fqxDXHzPu_vIquvhD0UmashmG2KEmL4cdJCct-OXvng"
}
```

<span style="color:orange;">**POST**</span> - Barista register
```
[POST]http://127.0.0.1:5000/auth/register
```
Description: Register new baristas and return authentication bearer token.<br><br>
**Request Body** (json)
```json
{
    "username":"barista3",
    "password":"*********",
    "first_name":"Kayla",
    "last_name":"T",
    "email":"kayla@email.com",
    "contact_number":"0433446677",
    "address":"2 Bunda st Canberra 2600"
}
```
*Example output:*
```json
{
    "username": "barista3",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NDY4NTEyMCwianRpIjoiOGU4NzZkOTgtMDRhNi00OTEyLWExNTgtYzVhMTc0YzRjYTNhIiwidHlwZSI6VzcyIsInN1YiI6InVzZXIzIiwibmJmIjoxNjY0Njg1MTIwLCJleHAiOjE2NjQ3NzE1MjB9.8-a2VnyUiCtsnquEv9PgdYn901gEe4IO0H2FArlBGaU"
}
```

<span style="color:orange;">**POST**</span> - Apply for job
```
[POST]http://127.0.0.1:5000/jobs/<job_id>/apply
```
Description: Barista apply for an available job.<br><br>
**Authorization** - Bearer Token ``<barista token>`` <br><br>
*Example request*
```
[POST]http://127.0.0.1:5000/jobs/1/apply
```

*Example output*
```json
{
    "id": 4,
    "job": {
        "id": 1,
        "description": "Barista required for busy cafe on Sunday",
        "date": "2022-09-22",
        "start_time": "10:00:00",
        "finish_time": "14:00:00",
        "pay_rate": 35,
        "status": "To be fulfilled",
        "barista": null,
        "venue": {
            "id": 1,
            "venue_name": "cafe1",
            "address": "12 Connell Way Belconnen ACT 2617",
            "city": "Canberra",
            "email": "info@cafe1.com",
            "abn": "180180180",
            "contact_number": "0261235678"
        }
    },
    "barista": {
        "id": 3,
        "first_name": "Kayla",
        "last_name": "T",
        "email": "kayla@email.com",
        "contact_number": "0433446677",
        "address": "2 Bunda st Canberra 2600",
        "rating": 0.0,
        "reviews": []
    },
    "status": "pending"
}
```

<span style="color:blue;">**PUT**</span> - Assign barista to job
```
[POST]http://127.0.0.1:5000/jobs/<job_id>/approve
```
Description: Assign chosen barista to the job and mark all other applications unsuccessful<br><br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
*Example request*
```
[POST]http://127.0.0.1:5000/jobs/1/approve
```
**Request Body** (json)
```json
{
    "barista_id":1
}
```
*Example output*
```json
{
    "id": 1,
    "description": "Barista required for busy cafe on Sunday",
    "date": "2022-09-22",
    "start_time": "10:00:00",
    "finish_time": "14:00:00",
    "pay_rate": 35,
    "status": "fulfilled",
    "barista": {
        "id": 1,
        "first_name": "Tom",
        "last_name": "Win",
        "email": "barista1@email.com",
        "contact_number": "04322445566",
        "address": "10 Bundy st, Canberra 2600",
        "rating": 0.0,
        "reviews": []
    },
    "venue": {
        "id": 1,
        "venue_name": "cafe1",
        "address": "12 Connell Way Belconnen ACT 2617",
        "city": "Canberra",
        "email": "info@cafe1.com",
        "abn": "180180180",
        "contact_number": "0261235678"
    }
}
```

<span style="color:green;">**GET**</span> - Get venues managed by current manager
```
[GET]http://127.0.0.1:5000/venues/
```
Description: Get all venues managed by current manager<br><br>

**Authorization** - Bearer Token ``<manager token>`` <br><br>

*Example output:*
```json
[
    {
        "id": 1,
        "venue_name": "cafe1",
        "address": "12 Connell Way Belconnen ACT 2617",
        "city": "Canberra",
        "email": "info@cafe1.com",
        "abn": "180180180",
        "contact_number": "0261235678",
        "manager": {
            "id": 1,
            "first_name": "Nick",
            "last_name": "Martin",
            "email": "nick@email.com",
            "contact_number": "0433332222"
        },
        "jobs": [
            {
                "id": 1,
                "description": "Barista required for busy cafe on Sunday",
                "date": "2022-09-22",
                "start_time": "10:00:00",
                "finish_time": "14:00:00",
                "pay_rate": 35,
                "status": "fulfilled",
                "barista": {
                    "id": 1,
                    "first_name": "Tom",
                    "last_name": "Win",
                    "email": "barista1@email.com",
                    "contact_number": "04322445566",
                    "address": "10 Bundy st, Canberra 2600",
                    "rating": 0.0,
                    "reviews": []
                }
            }
        ]
    }
]
```

<span style="color:red;">**GET**</span> - Delete a job
```
[DELETE]http://127.0.0.1:5000/jobs/delete/<job_id>
```
Description: Delete one job managed by current manager<br><br>

**Authorization** - Bearer Token ``<manager token>`` <br><br>
*Example request*
```
[DELETE]http://127.0.0.1:5000/jobs/delete/3
```
*Example output*
```json
{
    "id": 3,
    "description": "Helper barista needed!",
    "date": "2022-09-30",
    "start_time": "08:00:00",
    "finish_time": "15:00:00",
    "pay_rate": 50,
    "status": "To be fulfilled",
    "barista": null,
    "venue": {
        "id": 2,
        "venue_name": "cafe2",
        "address": "112 George St Sydney NSW 2000",
        "city": "Sydney",
        "email": "info@cafe2.com",
        "abn": "191191191",
        "contact_number": "0298765432"
    }
}
```

<span style="color:green;">**GET**</span> - Get all applications
```
[GET]http://127.0.0.1:5000/applications
```
Description: Get all applications associated with venues managed by current manager<br><br>

**Authorization** - Bearer Token ``<manager token>`` <br><br>

```json
[
    {
        "id": 1,
        "job": {
            "id": 1,
            "description": "Barista required for busy cafe on Sunday",
            "date": "2022-09-22",
            "start_time": "10:00:00",
            "finish_time": "14:00:00",
            "pay_rate": 35,
            "status": "fulfilled",
            "barista": {
                "id": 1,
                "first_name": "Tom",
                "last_name": "Win",
                "email": "barista1@email.com",
                "contact_number": "04322445566",
                "address": "10 Bundy st, Canberra 2600",
                "rating": 0.0,
                "reviews": []
            },
            "venue": {
                "id": 1,
                "venue_name": "cafe1",
                "address": "12 Connell Way Belconnen ACT 2617",
                "city": "Canberra",
                "email": "info@cafe1.com",
                "abn": "180180180",
                "contact_number": "0261235678"
            }
        },
        "barista": {
            "id": 1,
            "first_name": "Tom",
            "last_name": "Win",
            "email": "barista1@email.com",
            "contact_number": "04322445566",
            "address": "10 Bundy st, Canberra 2600",
            "rating": 0.0,
            "reviews": []
        },
        "status": "approved"
    },
    {
        "id": 2,
        "job": {
            "id": 1,
            "description": "Barista required for busy cafe on Sunday",
            "date": "2022-09-22",
            "start_time": "10:00:00",
            "finish_time": "14:00:00",
            "pay_rate": 35,
            "status": "fulfilled",
            "barista": {
                "id": 1,
                "first_name": "Tom",
                "last_name": "Win",
                "email": "barista1@email.com",
                "contact_number": "04322445566",
                "address": "10 Bundy st, Canberra 2600",
                "rating": 0.0,
                "reviews": []
            },
            "venue": {
                "id": 1,
                "venue_name": "cafe1",
                "address": "12 Connell Way Belconnen ACT 2617",
                "city": "Canberra",
                "email": "info@cafe1.com",
                "abn": "180180180",
                "contact_number": "0261235678"
            }
        },
        "barista": {
            "id": 2,
            "first_name": "Lee",
            "last_name": "Lee",
            "email": "barista2@email.com",
            "contact_number": "0411223344",
            "address": "12 Smith st, Canberra 2610",
            "rating": 0.0,
            "reviews": []
        },
        "status": "unsuccessful"
    },
    {
        "id": 4,
        "job": {
            "id": 1,
            "description": "Barista required for busy cafe on Sunday",
            "date": "2022-09-22",
            "start_time": "10:00:00",
            "finish_time": "14:00:00",
            "pay_rate": 35,
            "status": "fulfilled",
            "barista": {
                "id": 1,
                "first_name": "Tom",
                "last_name": "Win",
                "email": "barista1@email.com",
                "contact_number": "04322445566",
                "address": "10 Bundy st, Canberra 2600",
                "rating": 0.0,
                "reviews": []
            },
            "venue": {
                "id": 1,
                "venue_name": "cafe1",
                "address": "12 Connell Way Belconnen ACT 2617",
                "city": "Canberra",
                "email": "info@cafe1.com",
                "abn": "180180180",
                "contact_number": "0261235678"
            }
        },
        "barista": {
            "id": 3,
            "first_name": "Kayla",
            "last_name": "T",
            "email": "kayla@email.com",
            "contact_number": "0433446677",
            "address": "2 Bunda st Canberra 2600",
            "rating": 0.0,
            "reviews": []
        },
        "status": "unsuccessful"
    }
]
```

<span style="color:green;">**GET**</span> - Get current barista applications
```
[GET]http://127.0.0.1:5000/applications/user
```
Description: Get all applications associated current signed in barista<br><br>

**Authorization** - Bearer Token ``<barista token>`` <br><br>

*Example output*
```json
[
    {
        "id": 1,
        "job": {
            "id": 1,
            "description": "Barista required for busy cafe on Sunday",
            "date": "2022-09-22",
            "start_time": "10:00:00",
            "finish_time": "14:00:00",
            "pay_rate": 35,
            "status": "fulfilled",
            "venue": {
                "id": 1,
                "venue_name": "cafe1",
                "address": "12 Connell Way Belconnen ACT 2617",
                "city": "Canberra",
                "email": "info@cafe1.com",
                "abn": "180180180",
                "contact_number": "0261235678"
            }
        },
        "barista": {
            "id": 1,
            "first_name": "Tom",
            "last_name": "Win",
            "email": "barista1@email.com",
            "contact_number": "04322445566",
            "address": "10 Bundy st, Canberra 2600",
            "rating": 0.0,
            "reviews": []
        },
        "status": "approved"
    },
    {
        "id": 5,
        "job": {
            "id": 2,
            "description": "Barista wanted Saturday",
            "date": "2022-09-25",
            "start_time": "08:00:00",
            "finish_time": "16:00:00",
            "pay_rate": 35,
            "status": "To be fulfilled",
            "venue": {
                "id": 2,
                "venue_name": "cafe2",
                "address": "112 George St Sydney NSW 2000",
                "city": "Sydney",
                "email": "info@cafe2.com",
                "abn": "191191191",
                "contact_number": "0298765432"
            }
        },
        "barista": {
            "id": 1,
            "first_name": "Tom",
            "last_name": "Win",
            "email": "barista1@email.com",
            "contact_number": "04322445566",
            "address": "10 Bundy st, Canberra 2600",
            "rating": 0.0,
            "reviews": []
        },
        "status": "pending"
    }
]
```
<span style="color:red;">**DELETE**</span> - Delete pending application
```
[DELETE]http://127.0.0.1:5000/applications/user/<application_id>
```
Description: Delete pending application that made by current barista<br><br>

**Authorization** - Bearer Token ``<barista token>`` <br><br>

*Example request*
```
[DELETE]http://127.0.0.1:5000/applications/user/5
```
*Example output*
```json
{
    "id": 5,
    "job": {
        "id": 2,
        "description": "Barista wanted Saturday",
        "date": "2022-09-25",
        "start_time": "08:00:00",
        "finish_time": "16:00:00",
        "pay_rate": 35,
        "status": "To be fulfilled",
        "venue": {
            "id": 2,
            "venue_name": "cafe2",
            "address": "112 George St Sydney NSW 2000",
            "city": "Sydney",
            "email": "info@cafe2.com",
            "abn": "191191191",
            "contact_number": "0298765432"
        }
    },
    "barista": {
        "id": 1,
        "first_name": "Tom",
        "last_name": "Win",
        "email": "barista1@email.com",
        "contact_number": "04322445566",
        "address": "10 Bundy st, Canberra 2600",
        "rating": 0.0,
        "reviews": []
    },
    "status": "pending"
}
```

<span style="color:blue;">**PUT**</span> - Update venue details
```
[PUT]http://127.0.0.1:5000/venues/<venue_id>
```
Description: Update venue details with associate venue_id, only manager who is managing this venue can perform this operation. Manager can update all fields or only update chosen fields of the venue. <br><br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
*Example request*
```
[PUT]http://127.0.0.1:5000/venues/3
```
**Request Body** (json)
```json
{
    "venue_name":"Not cool cafe"
}
```

*Example output*
```json
{
    "id": 5,
    "venue_name": "Not cool cafe",
    "address": "101 Rock st Canberra 2612",
    "city": "canberra",
    "email": "info@coolcafe.com",
    "abn": "123456789",
    "contact_number": "0288888888",
    "manager": {
        "id": 3,
        "first_name": "James",
        "last_name": "Kelly",
        "email": "james@email.com",
        "contact_number": "0455661123"
    },
    "jobs": []
}
```
<span style="color:red;">**DELETE**</span> - Delete venue
```
[DELETE]http://127.0.0.1:5000/venues/<venue_id>
```
Description: Delete venue with the given venue id, venue need to be managed by current manager<br><br>

**Authorization** - Bearer Token ``<manager token>`` <br><br>

*Example request*
```
[DELETE]http://127.0.0.1:5000/venues/5
```

*Example output*
```json
{
    "id": 5,
    "venue_name": "Not cool cafe",
    "address": "101 Rock st Canberra 2612",
    "city": "canberra",
    "email": "info@coolcafe.com",
    "abn": "123456789",
    "contact_number": "0288888888",
    "manager": {
        "id": 3,
        "first_name": "James",
        "last_name": "Kelly",
        "email": "james@email.com",
        "contact_number": "0455661123"
    },
    "jobs": []
}
```

<span style="color:orange;">**POST**</span> - Create review
```
[POST]http://127.0.0.1:5000/jobs/<job_id>/review
```
Description: Manager create review for job performed by baristas, only fulfilled job can be reviewed.<br><br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
*Example request*
```
[POST]http://127.0.0.1:5000/jobs/1/review
```
**Request Body** (json)
```json
{
    "comments": "Good worker!",
    "rating": 5
}
```

*Example output*
```json
{
    "id": 1,
    "comments": "Good worker!",
    "rating": 5,
    "barista": {
        "id": 1,
        "first_name": "Tom",
        "last_name": "Win",
        "email": "barista1@email.com",
        "contact_number": "04322445566",
        "address": "10 Bundy st, Canberra 2600",
        "rating": 5.0
    },
    "job": {
        "id": 1,
        "description": "Barista required for busy cafe on Sunday",
        "date": "2022-09-22",
        "start_time": "10:00:00",
        "finish_time": "14:00:00",
        "pay_rate": 35,
        "status": "fulfilled",
        "venue": {
            "id": 1,
            "venue_name": "cafe1",
            "address": "12 Connell Way Belconnen ACT 2617",
            "city": "Canberra",
            "email": "info@cafe1.com",
            "abn": "180180180",
            "contact_number": "0261235678"
        }
    }
}
```

<span style="color:blue;">**PUT**</span> - Update reviews
```
[PUT]http://127.0.0.1:5000/reviews/<review_id>
```
Description: Update review that has been created. Manager can only update review that is created by themselves<br><br>
**Authorization** - Bearer Token ``<manager token>`` <br><br>
*Example request*
```
[PUT]http://127.0.0.1:5000/reviews/1
```
**Request Body** (json)
```json
{
    "comments":"Late for work!",
    "rating": 3
}
```

*Example output*
```json
{
    "id": 1,
    "comments": "Late for work!",
    "rating": 3,
    "barista": {
        "id": 1,
        "first_name": "Tom",
        "last_name": "Win",
        "email": "barista1@email.com",
        "contact_number": "04322445566",
        "address": "10 Bundy st, Canberra 2600",
        "rating": 3.0
    },
    "job": {
        "id": 1,
        "description": "Barista required for busy cafe on Sunday",
        "date": "2022-09-22",
        "start_time": "10:00:00",
        "finish_time": "14:00:00",
        "pay_rate": 35,
        "status": "fulfilled",
        "venue": {
            "id": 1,
            "venue_name": "cafe1",
            "address": "12 Connell Way Belconnen ACT 2617",
            "city": "Canberra",
            "email": "info@cafe1.com",
            "abn": "180180180",
            "contact_number": "0261235678"
        }
    }
}
```

<span style="color:red;">**DELETE**</span> - Delete review
```
[DELETE]http://127.0.0.1:5000/reviews/<review_id>
```
Description: Delete review with the given review id, review need to be managed by current manager<br><br>

**Authorization** - Bearer Token ``<manager token>`` <br><br>

*Example request*
```
[DELETE]http://127.0.0.1:5000/reviews/1
```

*Example output*
```json
{
    "id": 1,
    "comments": "Late for work!",
    "rating": 3,
    "barista": {
        "id": 1,
        "first_name": "Tom",
        "last_name": "Win",
        "email": "barista1@email.com",
        "contact_number": "04322445566",
        "address": "10 Bundy st, Canberra 2600",
        "rating": 3.0
    },
    "job": {
        "id": 1,
        "description": "Barista required for busy cafe on Sunday",
        "date": "2022-09-22",
        "start_time": "10:00:00",
        "finish_time": "14:00:00",
        "pay_rate": 35,
        "status": "fulfilled",
        "venue": {
            "id": 1,
            "venue_name": "cafe1",
            "address": "12 Connell Way Belconnen ACT 2617",
            "city": "Canberra",
            "email": "info@cafe1.com",
            "abn": "180180180",
            "contact_number": "0261235678"
        }
    }
}
```

<span style="color:green;">**GET**</span> - Get barista reviews
```
[GET]http://127.0.0.1:5000/reviews/barista/<barisa_id>
```
Description: Get all reviews associated with given barista id, viewable by managers<br><br>

**Authorization** - Bearer Token ``<manager token>`` <br><br>

*Example output*

```json
{
    "id": 1,
    "first_name": "Tom",
    "last_name": "Win",
    "email": "barista1@email.com",
    "contact_number": "04322445566",
    "rating": 4.0,
    "reviews": [
        {
            "id": 4,
            "comments": "Average worker!",
            "rating": 3
        },
        {
            "id": 5,
            "comments": "Good worker!",
            "rating": 5
        }
    ]
}
```

<span style="color:green;">**GET**</span> - Get barista information
```
[GET]http://127.0.0.1:5000/users
```
Description: Get barista information of current signed in barista<br><br>

**Authorization** - Bearer Token ``<barista token>`` <br><br>

*Example output*
```json
{
    "id": 1,
    "first_name": "Tom",
    "last_name": "Win",
    "email": "barista1@email.com",
    "contact_number": "04322445566",
    "address": "10 Bundy st, Canberra 2600",
    "rating": 4.0
}
```

<span style="color:blue;">**PUT**</span> - Update barista details
```
[PUT]http://127.0.0.1:5000/users
```
Description: Update user/barista details with associate bearer token, user may update certain fields of the job and leave other fields unchanged. <br><br>
**Authorization** - Bearer Token ``<barista token>`` <br><br>
**Request Body** (json)
```json
{
    "email": "tom@email.com",
    "address": "100 Cool place"
}
```

*Example output*
```json
{
    "id": 1,
    "first_name": "Tom",
    "last_name": "Win",
    "email": "tom@email.com",
    "contact_number": "04322445566",
    "address": "100 Cool place",
    "rating": 4.0
}
```

## References
Michael, B. (2022, July 14). Why use PostgreSQL as a Database for my Next Project in 2022. Retrieved 2022, Oct 1, from https://fulcrum.rocks/blog/why-use-postgresql-database

Mario, H. (2018, Dec 25). What is an ORM and Why You Should Use it. Retrieved 2022, Oct 1, from https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a