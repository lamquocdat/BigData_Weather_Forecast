from flask import render_template, jsonify
from bson import ObjectId
import datetime
from pymongo import DESCENDING
from database.mongodb import db

def home():
    predicts = list(db.predict_old_motobike.find().sort('predictedAt', DESCENDING))

    for predict in predicts:
        predicted_at = predict['predictedAt']
        predict['date'] = predicted_at.strftime('%d/%m/%Y')
        predict['time'] = predicted_at.strftime('%H:%M:%S')

    return render_template('home.html', **locals())

def getData():
    predicts = list(db.predict_old_motobike.find().sort('predictedAt', DESCENDING))
    result = []
    for predict in predicts:
        predict_dict = {}
        for key, value in predict.items():
            if isinstance(value, ObjectId):
                predict_dict[key] = str(value)
            elif isinstance(value, datetime.datetime):
                predict_dict[key] = value.isoformat()
                predict_dict['date'] = value.strftime('%d/%m/%Y')
                predict_dict['time'] = value.strftime('%H:%M:%S')
            else:
                predict_dict[key] = value

        result.append(predict_dict)

    # Trả về dữ liệu dưới dạng JSON
    return jsonify(result)