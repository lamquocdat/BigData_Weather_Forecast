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

# Tải model dự đoán thời tiết
weather_model_path = "app/models/weather/random_forest_model"
weather_model = PipelineModel.load(weather_model_path)

# Tải model dự đoán lượng mưa
rain_model_path = "app/models/amount_of_rain/logistic_regression_model"
rain_model = PipelineModel.load(rain_model_path)

# Hàm ánh xạ kết quả dự đoán thời tiết
def convert_prediction(value):
    if value == 1.0:
        return 'rain'
    elif  value == 0.0 :
        return 'no rain'
    
# Hàm ánh xạ kết quả dự đoán lượng mưa
def map_label_to_precipMM(prediction):
    mapping_dict = {
        0.0: 0.0, 1.0: 0.2, 2.0: 0.1, 3.0: 0.3, 4.0: 0.4, 5.0: 0.5, 6.0: 0.6, 7.0: 0.7, 8.0: 0.8, 9.0: 1.1, 
        10.0: 0.9, 11.0: 1.2, 12.0: 1.3, 13.0: 1.0, 14.0: 1.5, 15.0: 1.4, 16.0: 1.6, 17.0: 1.7, 18.0: 1.8, 19.0: 1.9, 
        20.0: 2.0, 21.0: 2.1, 22.0: 2.2, 23.0: 2.3, 24.0: 2.4, 25.0: 2.5, 26.0: 2.7, 27.0: 2.6, 28.0: 3.0, 29.0: 2.9, 
        30.0: 3.1, 31.0: 2.8, 32.0: 3.2, 33.0: 3.4, 34.0: 3.6, 35.0: 3.5, 36.0: 3.3, 37.0: 3.7, 38.0: 4.0, 39.0: 3.8, 
        40.0: 4.1, 41.0: 4.2, 42.0: 3.9, 43.0: 4.5, 44.0: 4.7, 45.0: 4.4, 46.0: 4.6, 47.0: 4.3, 48.0: 4.8, 49.0: 4.9, 
        50.0: 5.2, 51.0: 5.0, 52.0: 5.4, 53.0: 5.1, 54.0: 5.3, 55.0: 5.6, 56.0: 6.1, 57.0: 5.9, 58.0: 5.5, 59.0: 6.0, 
        60.0: 5.7, 61.0: 6.5, 62.0: 7.4, 63.0: 5.8, 64.0: 6.3, 65.0: 6.8, 66.0: 6.2, 67.0: 6.4, 68.0: 6.9, 69.0: 6.7, 
        70.0: 7.8, 71.0: 7.1, 72.0: 7.0, 73.0: 8.3, 74.0: 7.6, 75.0: 6.6, 76.0: 7.2, 77.0: 8.0, 78.0: 8.5, 79.0: 8.2, 
        80.0: 7.7, 81.0: 7.9, 82.0: 7.3, 83.0: 7.5, 84.0: 10.5, 85.0: 9.8, 86.0: 9.3, 87.0: 11.0, 88.0: 8.4, 89.0: 8.6, 
        90.0: 8.8, 91.0: 8.9, 92.0: 9.0, 93.0: 9.1, 94.0: 9.2, 95.0: 9.7, 96.0: 11.6, 97.0: 9.4, 98.0: 9.5, 99.0: 10.0, 
        100.0: 10.1, 101.0: 10.4, 102.0: 8.7, 103.0: 10.2, 104.0: 8.1, 105.0: 10.7, 106.0: 11.1, 107.0: 11.4, 108.0: 12.1, 109.0: 12.6, 
        110.0: 13.0, 111.0: 9.6, 112.0: 10.6, 113.0: 10.9, 114.0: 11.2, 115.0: 11.5, 116.0: 11.8, 117.0: 13.2, 118.0: 13.8, 119.0: 13.9, 
        120.0: 15.1, 121.0: 10.3, 122.0: 10.8, 123.0: 11.3, 124.0: 11.7, 125.0: 11.9, 126.0: 12.0, 127.0: 12.7, 128.0: 13.1, 129.0: 13.7, 
        130.0: 14.5, 131.0: 14.8, 132.0: 9.9, 133.0: 12.2, 134.0: 12.3, 135.0: 12.4, 136.0: 12.5, 137.0: 12.8, 138.0: 12.9, 139.0: 13.4, 
        140.0: 13.5, 141.0: 13.6, 142.0: 14.0, 143.0: 14.1, 144.0: 14.2, 145.0: 14.6, 146.0: 15.0, 147.0: 15.3, 148.0: 16.1, 149.0: 17.0, 
        150.0: 17.2, 151.0: 17.4, 152.0: 17.5, 153.0: 17.9, 154.0: 18.3, 155.0: 18.5, 156.0: 19.4, 157.0: 22.7, 158.0: 24.5, 159.0: 24.7, 
        160.0: 25.9, 161.0: 28.5, 162.0: 29.8, 163.0: 30.1, 164.0: 31.1, 165.0: 31.5, 166.0: 42.8
    }

    return mapping_dict.get(prediction, None)
    
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
    for message in consumer:
        # Chuyển các cột kiểu string mà có dạng số thành float
        numeric_columns = ['moon_illumination', 'time','tempC','tempF','windspeedMiles','windspeedKmph','winddirDegree', 'weatherCode','precipInches','humidity','visibility','visibilityMiles','pressure','pressureInches','cloudcover','HeatIndexC','HeatIndexF','DewPointC','DewPointF','WindChillC','WindChillF','WindGustMiles','WindGustKmph','FeelsLikeC','FeelsLikeF','uvIndex']
        for column in numeric_columns:
            float_value = float(message.value[column])
            message.value[column] = float_value

        predict_origin = message.value['predict']
        precipMM_origin = message.value['precipMM']

        current_time = datetime.now() 

        data = copy.deepcopy(message.value)
        data['createdAt'] = current_time
        data['updatedAt'] = current_time
        db.data.insert_one(data)

        # print(f"\nReceived message: \n{message.value}")

        # Dự đoán thời tiết
        weather_prediction = weatherPrediction(message.value, weather_model)

        # Kiểm tra nếu kết quả là mưa thì dự đoán lượng mưa, còn không mưa thì lượng mưa là 0
        weather_prediction[0]['predict'] = convert_prediction(weather_prediction[0].pop('prediction', None))
        if(weather_prediction[0]['predict'] == "rain"):
            rain_prediction = amountOfRain(weather_prediction[0], rain_model)
            
            rain_prediction[0]['rain_prediction'] = map_label_to_precipMM(rain_prediction[0].pop('prediction'))
            rain_prediction[0]['predict_origin'] = predict_origin
            rain_prediction[0]['precipMM_origin'] = precipMM_origin
            rain_prediction[0]['predictedAt'] = current_time

            db.predict.insert_one(rain_prediction[0])
        else:
            weather_prediction[0]['rain_prediction'] = 0
            weather_prediction[0]['predict_origin'] = predict_origin
            weather_prediction[0]['precipMM_origin'] = precipMM_origin
            weather_prediction[0]['predictedAt'] = current_time

            db.predict.insert_one(weather_prediction[0])