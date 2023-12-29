from flask import Blueprint, send_from_directory
import os

from app.controllers.HomeController import *

main = Blueprint('main', __name__)

@main.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'),
                               'favicon_io/favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/', methods=['GET'])
def home_route():
    return home()

@main.route('/getData', methods=['GET'])
def getData_route():
    return getData()