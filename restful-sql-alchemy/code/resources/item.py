from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3
import uuid

from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):
    @jwt_required()
    def get(self, _id):
        item = ItemModel.get_item_by_id(_id)
        if item:
            return {"data": item.json(), "message": "Item fetched"}
        return ItemModel.item_not_found(_id)

    def delete(self, _id):
        item = ItemModel.get_item_by_id(_id)
        if item:
            item.delete_item()
            return {'data': item.json(), 'message': f'Deleted item with id:[{_id}]'}
        else:
            return ItemModel.item_not_found(_id)

    def put(self, _id):
        parser = ItemModel.get_item_parser(True)
        data = parser.parse_args()

        item = ItemModel.get_item_by_id(_id)
        if item:
            item.price = data['price']
            item.name = data['name']
            item.store_id = data['store_id']
            item.save_item()

            return {'data': item.json(), 'message': 'Item was successfully updated'}
        else:
            return ItemModel.item_not_found(_id)


class Items(Resource):
    def get(self):
        try:
            data = ItemModel.get_all_items()
        except:
            return {"message": "An error occured while fetching list of items"}, 500
        return {'data': data, 'message': f'Fetched list of items'}

    def post(self):
        parser = ItemModel.get_item_parser(update=False)
        data = parser.parse_args()

        if data["store_id"]:
            store = StoreModel.get_store_by_id(data["store_id"])
            if store:
                item = ItemModel(**data)
                try:
                    new_item = item.save_item()
                except:
                    return {"message": "An error occured creating an item"}, 500

                # item = ItemModel.get_item_by_id(_id)
                return {'data': new_item.json(), 'message': f'Item was added'}, 201
            return StoreModel.store_not_found(data["store_id"])
