import jwt
import json
from sqlalchemy import exc
from marshmallow import ValidationError
from flask import Blueprint, jsonify, request, current_app

from .languages import Language
from topik_app.extensions import db
from topik_app.authorization.authenticate import all_routes_tokenized
from .serializer import language_schema, languages_schema, post_language_schema

languages = Blueprint('languages', __name__, url_prefix='/language')


# @languages.before_request
# def before_request(*args, **kwargs):
#     return all_routes_tokenized()


# GET All Languages
@languages.route("/", methods=['GET'])
def get_all_languages():
    languages = Language.query.all()
    result = languages_schema.dump(languages)
    return jsonify(result), 200


# GET Single Language
@languages.route("/<id>/", methods=['GET'])
def get_one_language(id):
    language = Language.query.filter_by(id=id).first()
    if language:
        # The return type is Instrumented List of SQLAlchemy
        # print(language.sets[0].set_name)
        result = language_schema.dump(language)
        return jsonify(result), 200
    else:
        return jsonify({"message": "No Language Found for the current credentials"}), 404


# Add A Language
@ languages.route("/add/", methods=['POST'])
def add_language():
    try:
        if request.method == 'POST':
            input_data = request.form
            data = json.dumps(input_data)
            schema = post_language_schema
            new_language = schema.load(json.loads(data))
            language_name = new_language['language_name']
            new_language = Language(language_name)
            db.session.add(new_language)
            db.session.commit()
            return language_schema.jsonify(new_language), 200

    except ValidationError as err:
        print(err.valid_data)
        return jsonify({"error": err.messages}), 400

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Langauge Already Exists"}), 401

    except:
        db.session.rollback()
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('%s Failed to edit the language' + err)
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500


# EDIT A Language
@ languages.route("/edit/<id>/", methods=['PUT'])
def edit_language(id):
    try:
        if request.method == 'PUT':
            input_data = request.form
            data = json.dumps(input_data)
            schema = post_language_schema
            new_language = schema.load(json.loads(data))

            language = Language.query.get(id)
            if language is not None:
                language.language_name = new_language['language_name']
                db.session.commit()
                return language_schema.jsonify(language), 200

            else:
                return jsonify({"message": "No Lnaguage Has Been Added for the provided credentials"}), 404

    except ValidationError as err:
        current_app.logger.error('%s failed to edit language')
        print(err.valid_data)
        return jsonify({"error": err.messages}), 400

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Langauge Already Exists"}), 401

    except:
        db.session.rollback()
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('%s Failed to edit the language' + err)
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500


# DELETE A Language
@ languages.route("/delete/<id>/", methods=['DELETE'])
def delete_language(id):
    language = Language.query.get(id)
    try:
        if language is not None:
            db.session.delete(language)
            db.session.commit()
            return post_language_schema.jsonify(language), 200

        else:
            return jsonify({"message": "No Language Found"}), 404

    except:
        db.session.rollback()
        traceback.print_exc()  # This prints the traceback to the console
        err = traceback.format_exc()
        current_app.logger.error('%s Failed to edit the language' + err)
        return jsonify({"message": "An Error Occured Please Try Again Later"}), 500
