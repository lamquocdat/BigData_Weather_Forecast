import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexerModel
from pyspark.sql.functions import col

def preprocess_data(data, model):
    spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()
    # df = spark.createDataFrame(data)
    df = spark.createDataFrame(pd.DataFrame([data]))

    # Chuyển các cột kiểu String (đang có dạng số như 25,37,...) thành float
    numeric_columns = ['tempC', 'windspeedKmph', 'humidity', 'pressure', 'cloudcover', 'precipMM']
    for column in numeric_columns:
        df = df.withColumn(column, col(column).cast("float"))

    # chuyển weatherDesc thành label bằng StringIndexer
    indexer = StringIndexerModel.load("app/utils/StringIndexer")
    df = indexer.transform(df)

    # Lọc ra các cột quan trọng
    assembler = VectorAssembler(inputCols=['tempC', 'windspeedKmph', 'humidity', 'pressure', 'cloudcover', 'precipMM'], outputCol='features')
    df = assembler.transform(df)

    # Dự đoán
    predictions = model.transform(df)
    predictions = predictions.select('prediction').collect()
    prediction_list = [row['prediction'] for row in predictions]

    prediction = prediction_list[0] if len(prediction_list) == 1 else prediction_list
    
    return prediction
