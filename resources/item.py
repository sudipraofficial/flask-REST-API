import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        required=True,
        type=float,
        help='Price field required'                    
    )
    
    parser.add_argument('store_id',
        required=True,
        type=int,
        help='store_id required for every store'                     
    )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json()
        
        return {"Message":"Item not found!!"}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"Message": "A item with the given name {0} already exists".format(name)}, 400
        
        data = Item.parser.parse_args()
        # data = request.get_json(silent=True)
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except Exception:
            return {"Message": "Error occurred while inserting item: " + name}
        
        return item.json(), 201
        
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        
        if item is None:
            return {"Message": "Item not found to delete!!"}
        else:
            item.delete_from_db()
            return {"Message": "Item {0} deleted successfully".format(name)}
        
    def put(self, name):
        data = self.parser.parse_args()
        
        #data = request.get_json()
        item = ItemModel.find_by_name(name)
        
        if item is  None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            
        item.save_to_db()
        
        return item.json()
            
            
class ItemList(Resource):
    
    def get(self):
        try:
            return {'items': [item.json() for item in ItemModel.query.all()]} 
        except Exception:
            return {'message': 'Could not retrieve all items.'}, 500