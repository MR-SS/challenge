
# Challenge

  

all challenge is about make gift coupon system for users that each user can only use one coupon.

  
  
  

## what features have i implemented on this program?

-  ****jwt authentication****

-  **throttling** api calls with **Redis**

- user action **logg**

- unit test with **pytest**

-

  

# Installation

  

1.git clone https://github.com/MR-SS/challenge.git

2. cd challenge

3.docker-compose up --build -d

now opn http://localhost:8000

  

## More detail about challenge

  

in this challenge i try to create super secure coupon system with python [FastApi](https://fastapi.tiangolo.com/).why i choose fastapi rather than other python frameworks , because:

  

-  **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs( i have to create all feature by myself )

-  **Intuitive**: Great editor support. Completion everywhere. Less time debugging.

-  **Interactive API docs**: Automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)

  

## Api calls

it's just simple app. just we have 4 api call:

  

1. login : get authentication token(jwt)

2. default : have two hard coded user in db ( sajjad ( admin = False ) , admin ( admin = True ))

3. generate-coupon : only admin can do it

4. submit-coupon : any user can submit coup

## Unit test

i make unit test with pytest framework that's help me to build unit test.

consider these things: 

 - all test file in pytest start with test_*
 - in any test case i  make empty database and  after finishing the test .i make function `drop_all(test_db)` to clear the db.
 - all file is in `router/test_api.py`except **race conditions**
 
 
  

### Security issue that i found during writing unit test:

first of all i need to have a copy of main database. so i create a test detabase for all my test cases and each test case test a vulnerability like DOS, api rate limt ,jwt attacks ( i user jwt for authorization) and the Big one race conditions ( i think the main point of the challenge is race conditions and how to prevent it )

## flow of all unit test:
 in all unit test . i make specific user with and the try to request other api call and check that have  successful  response or not . with **assert** command can check them
 
## detail about unit tests:

 - test_create_use : create successful user  and ( user is hard coded! )      
 `   http://localhost:8000/login`
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
 - go inside the we container with  `docker exec -it <container id> bash`
 - type `python -m pytest -vv`  ** make sure use  -m ** 

## Race condition 
Here, the main vulnerabillity is race condition. I make a file called `race_condition.py`. the hole point is db make a condition to check if user used a coupen before or not and after that make an insert query in that db. I test it in **sqlite** and in 10 parallel requests I got 8 race condition. interesting, isn't it?? as it where told in the challenge's doc, I have to use a production database . I used postgresql as my db. the I fired up my postgres in docker and try to attack and send request in parallel and postgres didn't get the race.just one row created in db ( i make a user_transaction table for check if user have a submited coupon or not )  so made sleep( 0.002) to make a delay in data base query and. now what ??  i have 2 row created in 200 request
 
### Race condition prevention flow:
In order to prevent from race condition I performed two different approaches. 
1- First, I used thread locks in python and using it, I locked the thread witch was responsible for checking if the user exists in the user-transaction database or not. So while this thread is procceing it's task, no other thread can execute. This way, two different threads can't execute simultaneously.
user-transaction database is the database with include users who submitted a coupon before.  So if a user exists in this database, he is not allowed to sumbit another coupon.
2- Since we are using APIs to implement the functionallity of the app, I considered it as a good practice to set an **API-limit** witch known as throttling in order to prevent bouth race condition and DDOS attacks. So I implemented it using redis.







