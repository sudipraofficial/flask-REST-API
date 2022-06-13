from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        required=True,
        type=float,
        help='Price field required'                    
    )
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "No such store!!"}, 400
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store %s already exists" % name}
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception:
            return {"message": "An Error occurred while saving"}, 500
        return {'messsage': 'Data Posted successfully'}, 200
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
                return {"message": "Store %s Deleted successfully"%name}
            except:
                return {"message": "An Error occurred while saving"}, 500
        return {"message": "Store %s does not exist" % name}
        
    
class StoreList(Resource):
    def get(self):
        try:
            return {"stores" : [store.json() for store in StoreModel.query.all()]}
        except:
            return  {"message": "An Error occurred while showing store list"}, 500