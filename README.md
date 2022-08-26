
# Challenge

  

all challenge is about make gift coupon system for users that each user can only use one coupon.

  
  
  

## what features this web application has?

-  ****jwt authentication****

-  **throttling** api calls with **Redis**

- User action **log**

- Unit test with **pytest**

- dockerized

  

# Installation

 
1.git clone https://github.com/MR-SS/challenge.git

2.cd challenge

3.docker-compose up --build -d

now open http://localhost:8000

### NOTE: make sure to create a  **.env**  file and add these variable for create a data base  
```
  POSTGRES_USERNAME=sajjad
  POSTGRES_PASSWORD=sajjad
  POSTGRES_DB=coupon
  ```
  

## More detail about challenge

  

in this challenge i try to create super secure coupon system with python [FastApi](https://fastapi.tiangolo.com/).why i choose fastapi rather than other python frameworks , because:

  

-  **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs( i have to create all feature by myself )

-  **Intuitive**: Great editor support. Completion everywhere. Less time debugging.

-  **Interactive API docs**: Automatic interactive API documentation ( provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)) 

  

## Api calls

it's just simple app. just we have 4 api call:

  

1. login : get authentication token(jwt)

2. default : have two hard coded user in db ( sajjad ( is_admin = False ) , admin ( is_admin = True ))

3. generate-coupon : only admin can do it

4. submit-coupon : any user can submit coup

## Using guide

Since we have two different roles in the web application (admin and user) we need to distinguish them and for this, I implemented an endpoint called /login witch is responsible for authenticating users. When a user sends a request to this endpoint along whit his credentials, if he exists in the database as a valid user, he will get a jason object including a **authorization token** witch is a **jwt token** in the response. So in further requests on behalf of this user, we can put this token in a specific header called **Authrization header** in order to keep the user logged in. It is good to note that we only have to include this header in those requests whitch requaire a user to be authorized. Since the implementation of my jwt token was a sample one, I wasn't able to connect it with swagger. So those request witch requaire authorization proccess (request to /generate-coupon & /submit-coupon) should trigger using curl.

    curl -X 'POST' 'http://localhost:8000/generate-coupon' -H 'Authrization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTY2MTM3NDA5Mn0.qO30l1oVuvR4-NLqmlBOxc9OGdElP4yqtOJL1vRqhUA' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "count": 1}'
>
    curl -X 'POST' 'http://localhost:8000/submit-coupon' -H 'Authrization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfYWRtaW4iOnRydWUsImV4cCI6MTY2MTM3NDA5Mn0.qO30l1oVuvR4-NLqmlBOxc9OGdElP4yqtOJL1vRqhUA' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "code": 1234}'

## Unit test

I make unit test with pytest framework that's help me to build unit test.

consider these things: 

 - all test file in pytest start with test_*
 - in any test case i  make empty database and  after finishing the test .i make function `drop_all(test_db)` to clear the db.
 - all file is in `router/test_api.py`except **race conditions**
 
 
### Security issue that i found during writing unit test:

first of all i need to have a copy of main database. so i create a test detabase for all my test cases and each test case test a vulnerability like DOS, api rate limt ,jwt attacks ( i user jwt for authorization) and the Big one race conditions ( i think the main point of the challenge is race conditions and how to prevent it . i will talk about later)

## flow of all unit test:
 in all unit test . i make specific user with and the try to request other api call and check that have  successful  response or not . with **assert** command can check them
 
## detail about unit tests:

 - test_create_use : create successful user  and ( user is hard coded! )      
 `http://localhost:8000/login`
 - test_submit_coupon : submit valid coupon
 - test_login_valid_user :  make a specific user and test it .if can login or not
 - test_login_invalid_user : it is clear
 - test_login_sqlinj : i have login page for users that  give user a specific jwt token . so i try to check if we have **sql injection** or not
 - test_generate_valid_coupon `http://localhost:8000/generate-coupon`
 - test_generate_infinity_coupon
 - test_add_invalid_count_in_generate_coupon
 - test_generate_coupon_no_token
 due to the presence of **jwt** .i tried to check the relevant vulnerability
 - test_none_alg_in_jwt :  (CVE-2015-9235)
 - test_change_is_admin_true_for_user_in_jwt_generate_coupon: jwt contain of username and is_admin key in it. i try to make a non admin user. and change the is_admin=True in it  and test the user  
 
 ## how to run these test
 
 - run the project with `docker-compose up --build -d` command 
 - go inside the we postgres container with  `docker exec -it <container id> bash`
 - psql -d <POSTGRES_DB=coupon>  -U <POSTGRES_USERNAME>   ( username and database name are in  .env file . for me was sajjad and coupon ) 
 - enter password ( in .env file)
 - CREATE DATABASE test;
 - exit from postgres container and run web container ( same as nmber 2 command => docker -exec -it <web container iD >  bash ) 
 - type `python -m pytest -vv`  ** make sure use  -m ** 

## Race condition 
Here, the main vulnerabillity is race condition. I make a file called `race_condition.py`. the hole point is db make a condition to check if user used a coupen before or not and after that make an insert query in that db. I test it in **sqlite** and in 10 parallel requests I got 8 race condition. interesting, isn't it?? as it where told in the challenge's doc, I have to use a production database. I used postgresql as my db. then I lunched my postgres in docker and tried to attack it and send a bunch of requests in parallel to it but the attack was not successful. just one row created in db (I make a user_transaction table to check if user have a submitted coupon or not). So, I set the sleep to 0.002 secounds to make a delay in data base query. now what?? as a resault, I have 2 row created in 200 requests so here, the attack was successful.
 

### User guide :
For tasting race conditions.first need to open  web docker container  And after that run race_condition.py




