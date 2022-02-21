from flask import Flask

webapp = Flask(__name__)

from app import main
from app import upload
from app import search
from app import list_keys
from app import configure
from app import statistics