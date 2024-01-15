import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexerModel
from pyspark.sql.functions import col

def weatherPrediction(data, model):
    spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()

    df = spark.createDataFrame(pd.DataFrame([data]))

    # Chuyển các cột kiểu String (đang có dạng số như 25,37,...) thành float
    numeric_columns = ['tempC', 'windspeedKmph', 'humidity', 'pressure', 'cloudcover', 'precipMM']
    for column in numeric_columns:
        df = df.withColumn(column, col(column).cast("float"))

    # chuyển weatherDesc thành label bằng StringIndexer
    indexer = StringIndexerModel.load("app/utils/weather/StringIndexer")
    df = indexer.transform(df)

    # Lọc ra các cột quan trọng
    assembler = VectorAssembler(inputCols=['tempC', 'windspeedKmph', 'humidity', 'pressure', 'cloudcover', 'precipMM'], outputCol='features')
    df = assembler.transform(df)

    # Dự đoán
    predictions = model.transform(df)
    predictions = predictions.select('prediction', 'weatherDesc').collect()

    result_list = [(row['prediction'], row['weatherDesc']) for row in predictions]

    return result_list

def amountOfRain(data, model):
    spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()

    df = spark.createDataFrame(pd.DataFrame([data]))

    # Chuyển các cột kiểu String (đang có dạng số như 25,37,...) thành float
    numeric_columns = ['weatherCode', 'cloudcover', 'humidity', 'pressure', 'pressureInches', 'tempC', 'tempF', 'uvIndex', 'visibility', 'visibilityMiles', 'windspeedKmph', 'winddirDegree']
    for column in numeric_columns:
        df = df.withColumn(column, col(column).cast("float"))

    # chuyển weatherDesc thành label bằng StringIndexer
    indexer = StringIndexerModel.load("app/utils/amount_of_rain/StringIndexer")
    df = indexer.transform(df)

    # Lọc ra các cột quan trọng
    assembler = VectorAssembler(inputCols=['weatherCode', 'cloudcover', 'humidity', 'pressure', 'pressureInches', 'tempC', 'tempF', 'uvIndex', 'visibility', 'visibilityMiles', 'windspeedKmph', 'winddirDegree'], outputCol='features')
    df = assembler.transform(df)

    # Dự đoán
    predictions = model.transform(df)
    predictions = predictions.select('prediction', 'precipMM').collect()
    
    result_list = [(row['prediction'], row['precipMM']) for row in predictions]

    return result_list