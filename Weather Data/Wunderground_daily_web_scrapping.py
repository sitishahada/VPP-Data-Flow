import time
from datetime import datetime, timedelta
import os


import pandas as pd
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Set up Firefox options for a headless browser
options = Options()
options.add_argument('--headless')
service = Service(executable_path='C:\Program Files\Geckodriver\geckodriver.exe')

# Function to fetch weather data
def fetch_weather_data(city, formatted_date, start_time, max_retries=10):
    url = f'https://www.wunderground.com/hourly/my/{city}/date/{formatted_date}'
    
    for attempt in range(max_retries):
        try:
            driver = webdriver.Firefox(options=options, service=service)
            driver.get(url)
            time.sleep(30)

            response = BS(driver.page_source, 'html.parser')
            table = response.find('table')
            list_condition = [data.get_text() for i in table.findAll('tr')
                              if (data := i.find('span', {'class': 'show-for-medium conditions'}))]

            driver.quit()

            df = pd.DataFrame()
            df['time'] = pd.date_range(start_time, periods=24, freq=pd.DateOffset(hours=1))
            df['Condition'] = list_condition
            df = df.replace({
                'Fair': 0, 
                'Mostly Clear': 0, 
                'Clear': 0, 
                'Sunny': 0, 
                'Mostly Sunny': 0,
                'Partly Cloudy': 1, 
                'Cloudy': 1, 
                'Mostly Cloudy': 1, 
                'Haze': 2, 
                'Mist': 3,
                'Fog': 4, 
                'Foggy': 4, 
                'Showers in the Vicinity': 5, 
                'Rain': 6, 
                'Few Showers': 7,
                'Showers': 7, 
                'Light Rain': 8, 
                'Light Rain Shower': 9, 
                'Light Rain with Thunder': 10, 
                'Thundershowers': 10,
                'Heavy Rain': 11, 
                'Heavy Rain Shower': 12, 
                'Thunder': 13, 
                'Thunderstorms': 14,
                'Heavy Thunderstorm': 15, 
                'Isolated Thunderstorms': 14, 
                'Scattered Thunderstorms': 14
            })
            df = df.set_index('time')
            df = df.resample('30min').ffill()

            # Directory creation
            directory = f'E:/0. VPP/0. VPP Migration Code/M5 dataset/{city.capitalize()}'
            os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist

            # Save to CSV
            csv_path = os.path.join(directory, f'{formatted_date}.csv')
            df.to_csv(csv_path, header=False)
            
            print(f"Data for {city.capitalize()} saved to {csv_path}")
            return df

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {city}: {e}")
            time.sleep(5)  # Optional: wait before retrying
        finally:
            try:
                driver.quit()
            except:
                pass
    print(f"Failed to fetch")

    # Main function
def main():
    start_date = datetime.now()
    current_date = start_date + timedelta(days=1)
    start_time = start_date.replace(hour=16, minute=0, second=0, microsecond=0)
    formatted_date = current_date.strftime("%Y-%m-%d")

    cities = ['kerteh', 'kuantan', 'permatang-pauh', 'malacca', 'segamat']
    for city in cities:
        fetch_weather_data(city, formatted_date, start_time)
    print('Ended')

if __name__ == "__main__":
    main()