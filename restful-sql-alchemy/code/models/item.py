import sqlite3
from flask_restful import reqparse
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.id = None
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"id": self.id, "name": self.name, "price": self.price, "store_id": self.store_id}

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

    @classmethod
    def get_all_items(cls):
        result = cls.query.all()
        data = [item.json() for item in result]
        return data

    @ classmethod
    def get_item_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @ classmethod
    def get_item_parser(cls, update=True):
        parser = reqparse.RequestParser()
        if update:
            parser.add_argument("price", type=float)
            parser.add_argument("name", type=str)
            parser.add_argument("store_id", type=int)
        else:
            parser.add_argument("price", type=float, required=True)
            parser.add_argument("name", type=str, required=True)
            parser.add_argument("store_id", type=int, required=True)
        return parser

    @ classmethod
    def item_not_found(cls, _id):
        return {'data': [], 'message': f'Item with id:[{_id}] was not found'}, 404
