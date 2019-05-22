#### ETLProject

Please look at example.py for usage reference

# Goals:
  Based off existing SQL database create Document based NoSQL database.

# Out:
  ## Per Team:
1. The name of the team.
2. The total number of goals scored by the team during the 2011 season.
3. The total number of wins the team earned during the 2011 season.
4. A histogram visualization of the team's wins and losses for the 2011 season (store the visualization directly).
5. The team's win percentage on days where it was raining during games in the 2011 season.  
  *5: Weather data is not available in the original database. Use DarkSky API to collect it.
### Assumptions
1. Only draws weather data from Berlin. This means some of the rain data will be inaccurate.
2. Does not attempt to match weather data with the specific time of the soccer match. Wins during rain only indicates that rain occured on the day.
# Tech:
1. SQL (Chris)
2. DarkSky API (Noah)
3. MongoDB (Noah)
4. Middleware (Chris/Noah)
# Process
DarkSky + SQL -> MongoDB



# Attributions:
[Powered by Dark Sky](https://darksky.net/poweredby/)
