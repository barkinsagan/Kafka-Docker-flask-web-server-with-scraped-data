from confluent_kafka import Consumer, KafkaException , KafkaError
import json
import sqlite3
import uuid

# Kafka consumer configuration

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': uuid.uuid4,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False  # Disable auto commit to manually commit offsets
}

consumer = Consumer(conf)
consumer.subscribe(['pokemon'])

# SQLite database configuration
conn = sqlite3.connect('/app/data/pokemon.db')
cursor = conn.cursor()





def insert_into_db(name, description, price, stock):
    cursor.execute('''
    INSERT OR REPLACE INTO pokemon (name, description, price, stock) VALUES (?, ?, ?, ?)
    ''', (name, description, price, stock))
    conn.commit()


try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            message = json.loads(msg.value().decode('utf-8'))
            name = message.get('name')
            print("Received information of " + name)
            description = message.get('Description')
            price = message.get('price')
            stock = message.get('stock')

            # Insert message data into database
            insert_into_db(name, description, price, stock)
            print([name, description, price, stock])
            # Commit offset after writing to file
            consumer.commit(msg)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    consumer.close()
    conn.close()

print("Consumer closed and database connection closed.")