import json

with open('open-weather-conditions-data.json') as conditions_data_file:
    conditions_data = json.load(conditions_data_file)

with open('open-weather-forecast-data.json') as forecast_data_file:
    forecast_data = json.load(forecast_data_file)

print("temp:  " + str(conditions_data[u'main'][u'temp']))
print("temp_min: " + str(conditions_data[u'main'][u'temp_min']))
print("main: " + str(conditions_data[u'weather'][0][u'main']))
# print("epoch: " +   str(conditions_data[u'current_observation'][u'observation_epoch']))

# print("today: " +   str(forecast_data[u'forecast'][u'txt_forecast'][u'forecastday'][0][u'title']))
print("today: " + str(forecast_data[u'list'][0]))
