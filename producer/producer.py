import uuid
import requests
import json
from kafka import KafkaProducer
import time
import logging



def get_data():
    try:
        response = requests.get("https://randomuser.me/api/", timeout=30)  # Thêm timeout để tránh treo
        response.raise_for_status()  
        res = response.json()
        return res['results'][0]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def format_data(res):
    if not res:  
        return {}

    location = res['location']
    data = {
        'id': str(uuid.uuid4()),
        'first_name': res['name']['first'],
        'last_name': res['name']['last'],
        'gender': res['gender'],
        'address': f"{location['street']['number']} {location['street']['name']}, "
                   f"{location['city']}, {location['state']}, {location['country']}",
        'post_code': location['postcode'],
        'email': res['email'],
        'username': res['login']['username'],
        'dob': res['dob']['date'],
        'registered_date': res['registered']['date'],
        'phone': res['phone'],
        'picture': res['picture']['medium']
    }

    return data

def stream_data():
    print('do0')
    time.sleep(30)
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000) #192.168.1.196   broker
    print('dô')
    count = 1
    
    while True:
        curr_time = time.time()
        time.sleep(10)
        if time.time() > curr_time + 120: #1 minute
            print('time out line 51')
            logging.warning('No data received from get_data()')
            continue
        try:
            res = get_data()

            if res is None:  # Kiểm tra nếu không lấy được dữ liệu
                logging.warning('No data received from get_data()')
                continue
            
            res = format_data(res)

            producer.send('users_created', json.dumps(res).encode('utf-8'))
            print(count)
            count += 1
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue
        
    
if __name__ == "__main__":
    logging.info("running")
    stream_data()

