import sqlite3
from flask_restful import reqparse
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name):
        self.id = None
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name, "items": [item.json() for item in self.items.all()]}

    def save_item(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        return self

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
        db.session.flush()
        return self

    @ classmethod
    def get_all_stores(cls):
        result = cls.query.all()
        data = [item.json() for item in result]
        return data

    @ classmethod
    def get_store_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @ classmethod
    def get_store_parser(cls, update=True):
        parser = reqparse.RequestParser()
        if update:
            parser.add_argument("name", type=str)
        else:
            parser.add_argument("name", type=str, required=True)
        return parser

    @ classmethod
    def store_not_found(cls, _id):
        return {'data': [], 'message': f'Store with id:[{_id}] was not found'}, 404
