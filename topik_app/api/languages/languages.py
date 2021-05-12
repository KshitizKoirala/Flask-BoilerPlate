from topik_app.extensions import db


class Language(db.Model):
    __tablename__ = 'language_table'

    id = db.Column(db.Integer, primary_key=True, )
    language_name = db.Column(db.String(80), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, language_name):
        self.language_name = language_name

    def __repr__(self):
        return '<Language %r>' % self.language_name
