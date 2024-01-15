from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
load_dotenv()
import os
from database.mongodb import db
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from app.services.predictServices import weatherPrediction, amountOfRain
import copy

spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()

# Tải model
weather_model_path = "app/models/weather/logistic_regression_model"
weather_model = PipelineModel.load(weather_model_path)

rain_model_path = "app/models/amount_of_rain/logistic_regression_model"
rain_model = PipelineModel.load(rain_model_path)

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
        data2 = copy.deepcopy(message.value)

        current_time = datetime.now() 

        data['createdAt'] = current_time
        data['updatedAt'] = current_time

        # Lưu vào database
        collection_old_car.insert_one(data)

        # print(f"\nReceived message: \n{message.value}")

        # Dự đoán
        weather_prediction = weatherPrediction(message.value, weather_model)
        prediction1, weatherDesc = weather_prediction[0]

        rain_prediction = amountOfRain(data2, rain_model)
        prediction2, precipMM = rain_prediction[0]

        predict_data = {
            'prediction_origin': prediction1,
            'prediction': weatherDesc,
            'rain_prediction': prediction2,
            'precipMM' : precipMM,
            'predictedAt': current_time
        }

        # print(f"\nPredict:\n{predict_data}")

        collection_predict.insert_one(predict_data)