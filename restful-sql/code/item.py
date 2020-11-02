from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
import sqlite3
import uuid


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
    @jwt_required()
    def get(self, _id):
        item = self.get_item_by_id(_id)
        if item:
            return {"data": item, "message": "Item fetched"}
        return self.item_not_found(_id)

    def delete(self, _id):
        item = self.get_item_by_id(_id)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE id=?"
            cursor.execute(query, (_id, ))
            connection.commit()
            connection.close()
            return {'data': item, 'message': f'Deleted item with id:[{_id}]'}
        else:
            return self.item_not_found(_id)

    def put(self, _id):
        parser = Utility.get_item_parser(True)
        data = parser.parse_args()

        item = self.get_item_by_id(_id)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            item.update(data)
            query = "UPDATE items SET name=?, price=? WHERE id=?"
            result = cursor.execute(
                query, (item['name'], item['price'], int(_id)))

            connection.commit()
            connection.close()

            return {'data': item, 'message': 'Item was successfully updated'}
        else:
            return self.item_not_found(_id)

    @classmethod
    def get_item_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE id=?"
        result = cursor.execute(query, (_id, ))
        row = result.fetchone()
        connection.close()
        if row:
            return {"id": row[0], "name": row[1], "price": row[2]}

    @classmethod
    def item_not_found(cls, _id):
        return {'data': [], 'message': f'Item with id:[{_id}] was not found'}, 404


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        data = []
        for row in result.fetchall():
            data.append({
                'id': row[0],
                'name': row[1],
                'price': row[2]
            })
        connection.commit()
        connection.close()
        return {'data':  data, 'message': f'Fetched list of items'}

    def post(self):
        parser = Utility.get_item_parser(update=False)
        data = parser.parse_args()

        try:
            self.add_item(data)
        except:
            return {"message": "An error occured creating an item"}, 500

        return {'data': data, 'message': f'Item was added'}, 201

    @classmethod
    def add_item(cls, data):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(NULL, ?, ?)"
        cursor.execute(query, (data["name"], data["price"]))

        connection.commit()
        connection.close()
