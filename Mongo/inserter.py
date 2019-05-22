#now to take a collection and confirm all entries are ready and then add them
from mongoentry import SoccerEntry
columns = ["name","2011_wins","visualization_png_binary","win_rate","2011_goals"]

def insert_soccer_panda_into_mongo_collection(pandas_df,mongo_collection):
    '''
    columns = ["name","2011_wins","visualization_png_binary","win_rate","2011_goals"]

    Takes a pandas dataframe formatted with the above columns and inserts it into supplied pymongo collection

    Params:
        pandas_df:
            Formatted Pandas DataFrame.
        mongo_collection:
            pymongo collection to be inserted into.
    '''
    entry_list = []
    pandas_df.apply(lambda x : row_into_entry_list(x,entry_list),axis=1)
    if any(map(lambda x : not SoccerEntry.ready(x) , entry_list)):
        raise ValueError("ERR: not all of the entries were ready")
    mongo_entries = [x.process_entry() for x in entry_list]
    mongo_collection.insert_many(mongo_entries)

def row_into_entry_list(row,entry_list):
    '''
    Converts Pandas row into SoccerEntry and adds the SoccerEntry to a list

    Params:
        row:
            row to be converted
        entry_list:
            list to add converted row into
    '''
    ent = SoccerEntry().name(row["name"]).visualization(row["visualization_png_binary"]).win_rate_on_rainy_days(row["win_rate_on_rainy_days"]).goals2011(row["2011_goals"]).wins2011(row["2011_wins"])
    entry_list.append(ent)
