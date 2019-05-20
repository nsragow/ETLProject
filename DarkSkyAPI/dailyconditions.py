import requests as r


class TimeMachine():
    '''
    Used to get historical data from Dark Sky API.
    Specifically draws out the precipitation type per day.

    Usage:
        tm = TimeMachine(dark_sky_api_key)
        response = tm.time_to_label_with_json(some_year,some_month,some_day)
        #precipitation label#
        print(response[0])
        #full JSON#
        print(response[1])
    '''
    lat = 52.520008
    lon = 13.404954
    def __init__(self, api_key):
        self.api_key = api_key

    def time_to_label_with_json(self,year,month,day):
        day = "{:0>2d}".format(day)
        month = "{:0>2d}".format(month)
        year = "{}".format(year)

        time = f"{year}-{month}-{day}T13:00:00"

        https = f"https://api.darksky.net/forecast/{self.api_key}/{self.lat},{self.lon},{time}?exclude=minutely,hourly,flags,currently"

        response = r.get(https)

        response_json = response.json()

        label = None
        err_msg = None
        if "daily" in  response_json.keys():
            #good
            daily = response_json["daily"]
            if "data" in daily:
                data = daily["data"]
                if len(data) > 0:
                    target_data = data[0]
                    if "precipType" in target_data:
                        label = target_data["precipType"]
                    else:
                        label = "none"
                else:
                    err_msg = "ERR: data array was empty"
            else:
                err_msg = "ERR: data not in daily"
        else:
            err_msg = "ERR: 'daily' not in response"

        if err_msg is not None:
            return err_msg
        return (label,response_json)
