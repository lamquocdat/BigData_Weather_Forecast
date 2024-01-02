from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
load_dotenv()
import os
from database.mongodb import db
from datetime import datetime
import joblib
from app.services.old_motobike_predict import preprocess_data

# Tải model và encoder
encoder_path = 'app/utils/encoder.joblib'
model_path = 'app/models/random_forest.joblib'

encoder = joblib.load(encoder_path)
model = joblib.load(model_path)

def create_consumer():
    topic_name = os.environ.get("KAFKA_TOPIC_NAME", "my_topic")
    server_name = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    group = os.environ.get("KAFKA_GROUP_ID", "my_group")

    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[server_name],
        auto_offset_reset='earliest',
        group_id=group,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

def consume_messages(consumer):
    collection_old_car = db.old_motobike
    collection_predict = db.predict_old_motobike

    for message in consumer:
        data = message.value

        current_time = datetime.now() 

        data['createdAt'] = current_time
        data['updatedAt'] = current_time

        # Lưu vào database
        collection_old_car.insert_one(data)

        # print(f"Received message: {data}")

        # Dự đoán
        prediction = preprocess_data(message.value, encoder, model)

        predict_data = {
            'prediction': prediction,
            'predictedAt': current_time
        }

        # print(f"Predict : {predict_data}")

        collection_predict.insert_one(predict_data)