import sys

sys.path.append('./Middleware')
sys.path.append('./Chris')

from csv_method import csv_to_pd

from middleware import Settings,panda_to_mongo

database_name = None
# "prac_db"
collection_name = None
# "prac_collection"
mongodb_client_loc = None
# 'mongodb://localhost:27017/'


settings = Settings(database_name,collection_name,mongodb_client_loc)

df = csv_to_pd("./Chris/project_2.csv")

panda_to_mongo(df,settings)
