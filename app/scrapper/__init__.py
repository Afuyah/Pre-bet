from flask import Blueprint

scraper = Blueprint('scraper', __name__)

from . import scraper