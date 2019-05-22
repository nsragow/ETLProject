from practice_data import get_without_viz
import sys
import pymongo
sys.path.append('./Visualization')
sys.path.append('./Mongo')
from visualization import append_visualizations
from inserter import insert_soccer_panda_into_mongo_collection

class Settings():
    '''
    Used in panda_to_mongo function to specify which
    pymongo collection should be inserted into.

    Ex./
        settings = Settings("Soccer_Stats","weather_and_visualizations","mongodb://localhost:27017/")

        panda_to_mongo(df,settings)
    '''
    def __init__(self,db_name,collection_name,mongo_client='mongodb://localhost:27017/'):
        self.db_name = db_name
        self.collection_name = collection_name
        self.mongo_client = mongo_client
def panda_to_mongo(df,settings):
    '''
    Takes properly formatted (see visualization.append_visualizations)
    Pandas DataFrame, adds a visualization column and the stores each
    row into the pymongo collection specified by settings.

    Params:
        df:
            the formatted Pandas Dataframe.
        settings:
            Settings object specifying the location of collection.
    '''
    append_visualizations(df)
    client = pymongo.MongoClient(settings.mongo_client)
    database = client[settings.db_name]
    collection = database[settings.collection_name]
    insert_soccer_panda_into_mongo_collection(df,collection)
