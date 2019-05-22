import sys

sys.path.append('./Middleware')
sys.path.append('./Chris')

from csv_method import csv_to_pd

from middleware import Settings,panda_to_mongo

settings = Settings("prac_db","prac_collection",'mongodb://localhost:27017/')

df = csv_to_pd("./Chris/project_2.csv")

panda_to_mongo(df,settings)
