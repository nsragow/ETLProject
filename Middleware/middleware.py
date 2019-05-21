from practice_data import get_without_viz
import sys
import pymongo
sys.path.append('./Visualization')
sys.path.append('./Mongo')
from visualization import append_visualizations
from inserter import insert_soccer_panda_into_mongo_collection

class Settings():
    def __init__(self,db_name,collection_name,mongo_client='mongodb://localhost:27017/'):
        self.db_name = db_name
        self.collection_name = collection_name
        self.mongo_client = mongo_client
def panda_to_mongo(df,settings):
    append_visualizations(df)
    client = pymongo.MongoClient(settings.mongo_client)
    database = client[settings.db_name]
    collection = database[settings.collection_name]
    insert_soccer_panda_into_mongo_collection(df,collection)
