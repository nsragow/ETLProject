import pandas as pd
from inserter import insert_soccer_panda_into_mongo_collection
import pymongo
rows = []
for x in range(200):
    row = []
    for y in range(5):
        row.append("dum_val")
    rows.append(row)
columns = ["name","2011_wins","visualization_png_binary","win_rate_on_rainy_days","2011_goals"]

df = pd.DataFrame(data=rows,columns=columns)

client = pymongo.MongoClient('mongodb://localhost:27017/')


database_collection_name = "aaabbbcccdddeeefff"
for_the_test = client[database_collection_name]
for_the_test = for_the_test[database_collection_name]
insert_soccer_panda_into_mongo_collection(df,for_the_test)
client.drop_database(database_collection_name)
insert_soccer_panda_into_mongo_collection(df,for_the_test)
cursor = for_the_test.find({})
count = 0
for x in cursor:
    count+=1
print(count)
assert count == 200
client.drop_database(database_collection_name)
