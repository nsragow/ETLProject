import requests as r


class TimeMachine():
    '''
    Used to get historical data from Dark Sky API.
    Specifically draws out the precipitation type per day.
    Each object keeps track of the originally supplied API key.
    Every subsequent call will draw from that key.

    Usage:
        tm = TimeMachine(dark_sky_api_key)
        response = tm.time_to_label_with_json(some_year,some_month,some_day)
        #precipitation label#
        print(response[0])
        #full JSON#
        print(response[1])
    '''
    # Lat and lon of Berlin, as per simplifying assumption.
    lat = 52.520008
    lon = 13.404954
    def __init__(self, api_key):
        '''
        Set the API key for subsequent calls.

        Params:
            api_key:
                String of API key associated with a Dark Sky account.
                All calls will draw from this API key.
        '''
        self.api_key = api_key

    def time_to_label_with_json(self,year,month,day):
        '''
        Given a date returns the weather label [rain/snow/none/...] along with the entire json response from Dark Sky.

        Params:
            year:
                Integer year of target date.
            month:
                Integer month of target date.
            day:
                Integer day of target date.
        Return:
            A tuple with the
                tuple[0] containing the target dates Dark Sky precipType label
                tuple[1] containing the json response for book keeping (this can be ignored)
            -OR-
            String err_msg if the json response did not contain the precipType in the expected location
        '''
        # first format integers to string, complying with API call standard
        # force whitespace on left of digit if only one digit
        day = "{:0>2d}".format(day)
        month = "{:0>2d}".format(month)
        # Year is assumed to be four digits long so it does not need formatting change
        year = "{}".format(year)

        # Specific time is unimportant. The only data that will be considered is the daily data anyways
        time = f"{year}-{month}-{day}T13:00:00"

        # Full API call
        # Do not need minutely,hourly,flags or currently data
        https = f"https://api.darksky.net/forecast/{self.api_key}/{self.lat},{self.lon},{time}?exclude=minutely,hourly,flags,currently"

        response = r.get(https)

        response_json = response.json()

        # will hold precipType label
        label = None
        # if any error is encountered while parsing it will be stored in here
        err_msg = None

        # precipType should be stored in:
        # json["daily"]["data"][0]["precipType"]
        # These nested loops confirm that the json has this structure.
        # If the json does not have this structure the err_msg will be filled with
        # appropirate error.
        if "daily" in  response_json.keys():
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

        # return err_msg if it was filled with a string (which implies
        # the json is structured in an unexpected way).
        if err_msg is not None:
            return err_msg
        else:
            return (label,response_json)
