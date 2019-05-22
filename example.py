import sys

sys.path.append('./Middleware')

from middleware import Settings,panda_to_mongo

settings = Settings("prac_db","prac_collection",'mongodb://localhost:27017/')

df = None

panda_to_mongo(df,settings)
