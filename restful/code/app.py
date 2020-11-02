from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import uuid

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'hello world'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Utility():
    @classmethod
    def get_item_parser(self, update=True):
        parser = reqparse.RequestParser()
        if update:
            parser.add_argument("price", type=float)
            parser.add_argument("name", type=str)
        else:
            parser.add_argument("price", type=float, required=True)
            parser.add_argument("name", type=str, required=True)
        return parser


class Item(Resource):
    @ jwt_required()
    def get(self, id):
        item_index = self.get_item_by_id(id)
        print('item_index', item_index)
        if item_index > -1:
            item = items[item_index]
            return {'data': item, 'message': f'Fetched item with id:[{id}]'}
        else:
            return self.item_not_found(id)

    def delete(self, id):
        item_index = self.get_item_by_id(id)
        if item_index > -1:
            items.pop(item_index)
            return {'data': items, 'message': f'Deleted item with id:[{id}]'}
        else:
            return self.item_not_found(id)

    def put(self, id):
        parser = Utility.get_item_parser(True)
        data = parser.parse_args()

        item_index = self.get_item_by_id(id)
        if item_index > -1:
            item = items[item_index]
            item.update(data)
            return {'data': item, 'message': 'Item was successfully updated'}
        else:
            return self.item_not_found(id)

    def get_item_by_id(self, id):
        filtered = [(idx, item)
                    for idx, item in enumerate(items) if item['id'] == id]
        if len(filtered) > 0:
            return filtered[0][0]
        else:
            return -1

    def item_not_found(self, id):
        return {'data': [], 'message': f'Item with id:[{id}] was not found'}, 404


class Items(Resource):
    def get(self):
        return {'data': items, 'message': f'Fetched list of items'}

    def post(self):
        parser = Utility.get_item_parser(update=False)
        data = parser.parse_args()
        data['id'] = str(uuid.uuid1())
        items.append(data)
        return {'data': data, 'message': f'Item was added'}, 201


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:id>')

app.run(port=5000, debug=True)
