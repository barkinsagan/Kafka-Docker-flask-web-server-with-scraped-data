import requests
from bs4 import BeautifulSoup
from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
import json
import time


conf = {
    'bootstrap.servers': 'kafka:9092',  
    'client.id': 'test'
}


admin_client = AdminClient(conf)

topic_name = "pokemon"
num_partitions = 3
replication_factor = 1


try:
    topic_list = [NewTopic(topic_name, num_partitions, replication_factor)]
    fs = admin_client.create_topics(topic_list)
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print(f"Topic '{topic}' created successfully.")
        except KafkaException as e:
            print(f"Failed to create topic '{topic}': {e}")
except KafkaException as e:
    print(f"Topic '{topic_name}' already exists.")

def get_spec_pokemon_json(url, name):
    pokemon_url = url + name
    pokemon_response = requests.get(pokemon_url)
    pokemon_soup = BeautifulSoup(pokemon_response.text, 'html.parser')

    desc_div = pokemon_soup.find('div', class_="woocommerce-product-details__short-description")
    desc = desc_div.find("p").get_text()

    price = pokemon_soup.find_all('span', class_="woocommerce-Price-amount amount")[1].get_text()

    stock = pokemon_soup.find('p', class_="stock in-stock").get_text()

    current_pokemon_json = {
        "name": name,
        "Description": desc,
        "price": price,
        "stock": stock
    }

    return current_pokemon_json

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

producer = Producer({
    'bootstrap.servers': 'kafka:9092' 
    
    
})

topic = "pokemon"
url = 'https://scrapeme.live/shop/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('h2', class_='woocommerce-loop-product__title')
    pokemon_names = [title.get_text(strip=True) for title in titles]

    for name in pokemon_names:
        try:
            current_json = get_spec_pokemon_json(url, name)
        except Exception as e:
            print("Error occured getting the  " + name)
           

        producer.produce(topic, value=json.dumps(current_json).encode('utf-8'), callback=delivery_report)

        print(f"Sent message: {current_json}")
        time.sleep(1)
        

    producer.flush()