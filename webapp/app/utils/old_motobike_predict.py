import pandas as pd

def preprocess_data(data, encoder, model):
    df = pd.DataFrame([data])

    # Lọc ra các cột quan trọng
    categorical_columns = ['volume', 'type', 'origin', 'automaker', 'series']

    df = df[categorical_columns]
   
    # Xử lý dữ liệu bằng encoder
    if categorical_columns:
        df_categorical = pd.DataFrame(encoder.transform(df[categorical_columns]).toarray(),
                                      columns=encoder.get_feature_names_out(categorical_columns))
        df = df.drop(categorical_columns, axis=1)
        df = pd.concat([df, df_categorical], axis=1)

    # Dự đoán
    predictions = model.predict(df)
    prediction = predictions[0] if len(predictions) == 1 else predictions.tolist()
    
    return prediction
