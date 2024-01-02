from flask import Blueprint, send_from_directory
import os

from app.controllers.HomeController import *

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home_route():
    return home()

@main.route('/getData', methods=['GET'])
def getData_route():
    return getData()

@main.route('/<path:undefined_path>', methods=['GET'])
def notfound_route(undefined_path):
    return notfound()