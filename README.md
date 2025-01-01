This is a very simple app that hit the open meteo API to calculate how many seconds of daylight were gained or lost on a given day compared to the previous day in Paris France.
The value is cached in valkey to avoid hitting the API more than once a day which is all that is needed.
