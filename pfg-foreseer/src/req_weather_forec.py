# %%
#Downloading weather data using Python as a CSV using the Visual Crossing Weather API
#See https://www.visualcrossing.com/resources/blog/how-to-load-historical-weather-data-using-python-without-scraping/ for more information.
import csv
import codecs
import urllib.request
import urllib.error
import sys
import pandas as pd
import pathlib
from dotenv import load_dotenv

#create data path if it does not exist
data_path = pathlib.Path.cwd().joinpath('../data')
#if not exist, create the directory
if not data_path.exists():
    data_path.mkdir(parents=True)

weather_forecast_path = data_path.joinpath('hist_weather_forecast/')
if not weather_forecast_path.exists():
    weather_forecast_path.mkdir(parents=True)
    
#Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv('APIKEY')

#%%
def req_weather_forec(apiKey, location, startDate='', endDate='', unitGroup='metric', 
                      contentType='csv', include='hours', forecastBasisDate='') -> pd.DataFrame:
    '''
    Function to request weather forecast data from Visual Crossing Weather API
    Parameters:
    - apiKey: str, API key
    - location: str, location for the weather data
    - startDate: str, optional, start date for the weather data. 
      If start date only is specified, a single historical or forecast day will be retrieved
    - endDate: str, optional, end date for the weather data
      If both start and and end date are specified, a date range will be retrieved
      If nothing is specified, the forecast is retrieved.
    - unitGroup: str, optional, sets the units of the output - us or metric
    - contentType: str, optional, JSON or CSV. JSON format supports daily, hourly, current conditions, 
      weather alerts and events in a single JSON package. CSV format requires an 'include' parameter 
      below to indicate which table section is required
    - include: str, optional, values include days,hours,current,alerts
    - forecastBasisDate: str, optional, date for the forecast basis
    Returns:
    - df: pandas dataframe, weather forecast data
    '''
    
    print(' - Requesting weather for: {}'.format(location))
    baseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    apiQuery = baseURL + location
    if len(startDate):
        apiQuery += '/' + startDate
        if len(endDate):
            apiQuery += '/' + endDate
    apiQuery += '?'
    
    if len(unitGroup):
        apiQuery += '&unitGroup=' + unitGroup
    if len(contentType):
        apiQuery += '&contentType=' + contentType
    if len(include):
        apiQuery += '&include=' + include
    if len(forecastBasisDate):
        apiQuery += '&forecastBasisDate=' + forecastBasisDate
    
    apiQuery += '&key=' + apiKey
    print(' - Running query URL: ')
    print()
    
    try:
        csvBytes = urllib.request.urlopen(apiQuery)
    except urllib.error.HTTPError as e:
        errorInfo = e.read().decode()
        print('Error code: ', e.code, errorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        errorInfo = e.read().decode()
        print('Error code: ', e.code, errorInfo)
        sys.exit()
        
    # Parse the results as CSV
    csvText = csv.reader(codecs.iterdecode(csvBytes, 'utf-8'))
    
    #Save CSVText in a dataframe, use the first row as header
    df = pd.DataFrame(csvText)
    df.columns = df.iloc[0]
    #remove first row
    df = df[1:]

    return df

#%%
Location='Durham,NC'
#get current weather forecast data
now = pd.Timestamp.now()
df_weather_forec = req_weather_forec(API_KEY, Location)
print(df_weather_forec.head())

#%%
#Saving the weather forecast data to a CSV file

now_str = now.strftime('%Y%m%d_%H%M') #convert timestamp to string, with format YYYYMMDD_HHMM
df_weather_forec.to_csv(weather_forecast_path.joinpath('weather_forecast_{}.csv'.format(now_str)), index=False)


#%%
#Historical weather forecast data can be retrieved by setting the start and end dates
#URL example:
#https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK/2023-05-01/2023-05-15?unitGroup=us&key=YOUR_API_KEY&include=days&forecastBasisDate=2023-05-01

startDate='2024-09-25'
endDate='2024-09-27'
forecastBasisDate='2024-09-25'

df_hist_weather_forec = req_weather_forec(apiKey= API_KEY, location = Location, startDate = startDate, 
                                          endDate = endDate, forecastBasisDate = forecastBasisDate)

# If there are no CSV rows then something fundamental went wrong
if len(df_hist_weather_forec) == 0:
    print('Sorry, but it appears that there was an error connecting to the weather server.')
    print('Please check your network connection and try again..')

# If there is only one CSV  row then we likely got an error from the server
elif len(df_hist_weather_forec) == 1:
    print('Sorry, but it appears that there was an error retrieving the weather data.')
    print('Error: ', FirstRow)
