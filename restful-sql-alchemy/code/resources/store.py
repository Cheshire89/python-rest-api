from db import db
from models.store import StoreModel
from flask_restful import Resource


class Store(Resource):
    def get(self, _id):
        store = StoreModel.get_store_by_id(_id)
        if store:
            return {"data": store.json(), "message": "Store fetched"}
        return StoreModel.store_not_found(_id)

    def delete(self, _id):
        store = StoreModel.get_store_by_id(_id)
        if store:
            store.delete_item()
            return {'data': store.json(), 'message': f'Deleted store with id:[{_id}]'}
        else:
            return StoreModel.store_not_found(_id)

    def put(self, _id):
        parser = StoreModel.get_store_parser(True)
        data = parser.parse_args()

        item = StoreModel.get_store_by_id(_id)
        if item:
            item.name = data['name']
            item.save_item()

            return {'data': item.json(), 'message': 'Store was successfully updated'}
        else:
            return StoreModel.store_not_found(_id)


class Stores(Resource):
    def get(self):
        try:
            data = StoreModel.get_all_stores()
        except:
            return {"message": "An error occured while fetching list of stores"}, 500
        return {'data': data, 'message': f'Fetched list of stores'}

    def post(self):
        parser = StoreModel.get_store_parser(update=False)
        data = parser.parse_args()
        item = StoreModel(**data)
        try:
            store = item.save_item()
        except:
            return {"message": "An error occured creating a Store"}, 500

        return {'data': store.json(), 'message': f'Store was added'}, 201
