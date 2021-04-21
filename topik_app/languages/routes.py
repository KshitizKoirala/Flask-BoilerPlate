from flask import Blueprint, jsonify
from .languages import Language

languages = Blueprint('languages', __name__, url_prefix='/language')


@languages.route("/")
def get_all():
    languages = Language.query.all()
    if languages:
        return languages
    else:
        return jsonify({"message": "No Language Has Been Added"}), 404
