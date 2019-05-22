class SoccerEntry():
    '''
    Class for organizing entry data to later be inserted into mongodb.

    Usage:
        ent = SoccerEntry().name("Galaxy").wins2011(10).visualization(None).win_rate_on_rainy_days(.3).goals2011(302)
        if ent.ready():
            print(ent.process_entry)
        else:
            print("missing some values")
    '''
    def __init__(self):
        self.pairs = dict()
    def name(self,name):
        '''
        Setter for name
        '''
        self.pairs["name"] = name
        return self
    def wins2011(self,win_count):
        '''
        Setter for 2011_wins
        '''
        self.pairs["2011_wins"] = win_count
        return self
    def visualization(self,visualization):
        '''
        Setter for visualization_png_binary
        '''
        self.pairs["visualization_png_binary"] = visualization
        return self
    def win_rate_on_rainy_days(self,win_rate):
        '''
        Setter for win_rate_on_rainy_days
        '''
        self.pairs["win_rate_on_rainy_days"] = win_rate
        return self
    def goals2011(self,goal_count):
        '''
        Setter for 2011_goals
        '''
        self.pairs["2011_goals"] = goal_count
        return self
    def ready(self):
        '''
        Return:
            True if all expected keys are present.
            False otherwise.
        '''
        status = True
        for key in ["name","2011_wins","visualization_png_binary","win_rate_on_rainy_days","2011_goals"]:
            if key not in self.pairs:
                status = False
                break
        return status
    def process_entry(self):
        '''
        Exceptions:
            ValuesError:
                if ran while ready() == False
        Return:
            Dict with all expected keys and their values.
        '''
        if not self.ready():
            raise ValueError("tried to process entry when the entry was missing values")
        return dict(self.pairs)
