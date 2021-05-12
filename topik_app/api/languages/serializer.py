from marshmallow import fields, validate

from topik_app.extensions import ma
from topik_app.api.languages.languages import Language
# from topik_app.api.question_sets.serializer import SetSchema


# GET LANGUAGE SCHEMA
class LanguageSchema(ma.Schema):

    class Meta:
        model = Language
        fields = ('id', 'language_name')


# GET NESTED LANGUAGE SCHEMA TO INCLUDE ALL THE FOREIGN KEY DATA
# class NestedLanguageSchema(ma.Schema):
#     sets = fields.Nested(SetSchema(many=True))

#     class Meta:
#         model = Language
#         fields = ('id', 'language_name', 'sets')


# POST LANGUAGE SCHEMA
class PostLanguageSchema(ma.Schema):
    language_name = fields.Str(required=True, validate=[
        validate.Length(min=4, max=100)])

    class Meta:
        fields = ('language_name', )


# Initialize the Schema
language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)
post_language_schema = PostLanguageSchema()
