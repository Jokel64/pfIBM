import python_weather
import asyncio
import paho.mqtt.publish as publish
from datetime import datetime




async def get_weather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.METRIC)

    # fetch a weather forecast from a city
    weather = await client.find("Stuttgart")

    cloudy = 0.0

    if weather.current.sky_code in [0, 1, 2, 3, 4, 17, 35, 37, 38, 47]:
        cloudy = 0.9
        #thunderstorm
    if weather.current.sky_code in [5, 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 18 , 40 , 39 , 45]:
        cloudy = 0.7
        #light rain/rain/light snow
    if weather.current.sky_code in [14 , 16 , 42 , 43 , 15 , 21 , 20 , 19 , 22 , 41 , 46]:
        cloudy = 0.8
        #heavier rain/snow/fog
    if weather.current.sky_code in [23 , 24 , 25 , 31 , 32 , 36]:
        cloudy = 0.2
        #clear
    if weather.current.sky_code in [27 , 29 , 33 , 28]:
        cloudy = 0.6
        #mostly cloudy
    if weather.current.sky_code in [26]:
        cloudy = 0.7
        #cloudy
    if weather.current.sky_code in [30 , 34]:
        cloudy = 0.3
        #partly sunny

    now = datetime.now()

    current_hour = int(now.strftime("%H"))
    if 6 < current_hour <= 8:
        sun_lux = 5000
    elif 8 < current_hour <= 20:
        sun_lux = 50000
    elif 20 < current_hour <= 22:
        sun_lux = 5000
    else:
        sun_lux = 5

    if cloudy != 0.0:
        publish.single("/weather", str(cloudy)+str(sun_lux)+str(weather.current.temperature))
        print(f"published: cloudy: {cloudy}, sun_lux: {sun_lux}, temp: {weather.current.temperature}")
    else:
        print("did not attempt publish since weather data did not load")

    # returns the current day's forecast temperature (int)
    print(f"current weather for {weather.current.observation_point}: temp: {weather.current.temperature}, sky: {weather.current.sky_text}, sky_code: {weather.current.sky_code} humidity: {weather.current.humidity}, wind: {weather.current.wind_display}")
    # get the weather forecast for a few days
    #for forecast in weather.forecasts:
    #    print(f"forecast date: {str(forecast.date)}, sky: {forecast.sky_text}, mean temp: {forecast.temperature}, low temp: {forecast.low}, high temp: {forecast.high}, precipitation value: {forecast.precip}")

    #publish.single("/weather", {"cloudy": 0.8, "sun_lux": 50000, "temp": 20})
    # close the wrapper once done
    await client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_weather())
