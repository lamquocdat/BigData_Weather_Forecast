from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
load_dotenv()
import os
from database.mongodb import db
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from app.services.predictServices import preprocess_data
import copy

spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()

# Tải model
model_path = "app/models/logistic_regression_model"
model = PipelineModel.load(model_path)

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
    collection_old_car = db.data
    collection_predict = db.predict

    for message in consumer:
        data = copy.deepcopy(message.value)

        current_time = datetime.now() 

        data['createdAt'] = current_time
        data['updatedAt'] = current_time

        # Lưu vào database
        collection_old_car.insert_one(data)

        # print(f"\nReceived message: \n{message.value}")

        # Dự đoán
        prediction = preprocess_data(message.value, model)

        label_to_weatherDesc = {
            8.0: "Heavy rain at times",
            2.0: "Cloudy",
            3.0: "Overcast",
            4.0: "Sunny",
            6.0: "Moderate or heavy rain shower",
            0.0: "Partly cloudy",
            7.0: "Moderate rain at times",
            1.0: "Patchy rain possible",
            5.0: "Clear",
            15.0: "Patchy light drizzle",
            10.0: "Mist",
            19.0: "Patchy light rain",
            17.0: "Torrential rain shower",
            20.0: "Thundery outbreaks possible",
            11.0: "Light drizzle",
            13.0: "Light rain",
            12.0: "Fog",
            14.0: "Moderate rain",
            16.0: "Patchy light rain with thunder",
            18.0: "Heavy rain",
            9.0: "Light rain shower"
        }

        weather_description = label_to_weatherDesc.get(prediction, "Unknown")

        predict_data = {
            'prediction_origin': prediction,
            'prediction': weather_description,
            'predictedAt': current_time
        }

        # print(f"\nPredict:\n{predict_data}")

        collection_predict.insert_one(predict_data)