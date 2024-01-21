import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def weatherPrediction(data, model):
    spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()

    df = spark.createDataFrame(pd.DataFrame([data]))

    predictions = model.transform(df)
    
    result_list = [row.asDict() for row in predictions.select([col for col in predictions.columns if col not in ['label', 'features', 'rawPrediction', 'probability']]).collect()]

    return result_list

def amountOfRain(data, model):
    spark = SparkSession.builder.appName("BigData_Weather_Forecast").getOrCreate()

    df = spark.createDataFrame(pd.DataFrame([data]))

    predictions = model.transform(df)

    result_list = [row.asDict() for row in predictions.select([col for col in predictions.columns if col not in ['label', 'features', 'rawPrediction', 'probability']]).collect()]

    return result_list