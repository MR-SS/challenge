   
   
from database.models import User_transaction
from database.hash import Hash
from database.models import Dbuser   
from database.db import SessionLocal
import requests
import grequests
import random


base_url ='http://localhost:8000'
username = 'mamad' + str(random.randint(100000, 999999))

if __name__ == '__main__':
    db = SessionLocal()
    db.add(Dbuser(
        username=username,
        password=Hash.bcrypt("admin"),
        is_admin=True
    ))
    db.commit()
    print('created user: ', username)
    response =requests.post(
        base_url + "/login",
        json={
            "username": username,
            "password": "admin"
        },
    )
    get_token = response.json().get("access_token")
    # std_handler = logging.StreamHandler()
    # std_handler.setLevel(logging.INFO)
    # logging.basicConfig(handlers=[std_handler], level=logging.DEBUG)
    # logging.info("sallam")
    generate_response = requests.post(
        base_url + "/generate-coupon",
        headers={
            "Authrization" : get_token
        },
        json={"count": 3}
    )
    print(generate_response.json())
    coupon_code = generate_response.json()[0]["code"]
    # submit_response = requests.post(
    #     "/submit-coupon",
    #     headers={
    #         "Authrization" : get_token
    #     },
    #     json={"code": coupon_code }
    # )
    url= []
    for i in range(200):
        rs = grequests.post(base_url + "/submit-coupon",
            headers={
            "Authrization" : get_token
            },
            json={"code": coupon_code }
        )
        url.append(rs)
    # databasetabe orint  ba sleep 1 
    # badesh print ba hamoon add
    # for resp in grequests.imap(url):
    results = grequests.map(url)
    row_numver =db.query(User_transaction).filter_by(user_name = username).count()
    print('created records: ', row_numver)
    assert row_numver == 1
