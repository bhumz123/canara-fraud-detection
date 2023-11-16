import json
import kafka.errors
from flask import Flask, request
from kafka import KafkaProducer
from db_manager.database import PostgreClient
from encryptor import encrypt
import uuid

db_client = PostgreClient()
try:
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], acks='all',
                             value_serializer=lambda m: json.dumps(m).encode('utf-8'), batch_size=0,
                             retries=2147483647, request_timeout_ms=300000, max_in_flight_requests_per_connection=1)
    print("Connection to Kafka successful")
except kafka.errors.BrokerNotAvailableError:
    print("Cannot connect to kafka client")

app = Flask(__name__)

def encrypt_data(data):
    data['cc_num'] = encrypt.encrypt_cc_num(data['cc_num'])
    data['merchant'] = encrypt.encrypt_merchant(data['merchant'])
    data['cust_locn'] = encrypt.encode_geohash(latitude=data['lat'], longitude=data['long'])
    data['merchant_locn'] = encrypt.encode_geohash(latitude=data['merch_lat'], longitude=data['merch_long'])
    data.pop('lat')
    data.pop('long')
    data.pop('merch_lat')
    data.pop('merch_long')
    return data


@app.route("/canara/stream/send_event", methods=['POST'])
def send_event():
    key_guid = uuid.uuid4()
    try:
        event = request.get_json()
    except json.decoder.JSONDecodeError as err:
        print("Invalid json request", err)
        return json.dumps({"message": "Invalid json request, please send proper json data"}), 400

    encrypted_event = encrypt_data(event)
    # print(encrypted_event)
    # sending encrypted data to database with uuid and status
    # print(type(encrypted_event['trans_date_trans_time']))
    res = db_client.send_to_db(encrypted_event['trans_date_trans_time'], key_guid, encrypted_event)
    if res == 0:
        event.update({"event_key": str(key_guid)})
        # sending encrypted data to kafka
        ack = producer.send(topic='testc', value=encrypted_event).get()
        print("Sent to kafka topic amex-source")
        if ack:
            return json.dumps({"message": "OK"}), 200
    elif res == 1:
        return json.dumps({"message": "An error occurred in server"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
