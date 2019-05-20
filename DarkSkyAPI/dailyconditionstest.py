import dailyconditions
import sys
#give api key as first argument

api_key = sys.argv[1]

tm = dailyconditions.TimeMachine(api_key)

print(tm.time_to_label_with_json(2012,1,7)[0])
