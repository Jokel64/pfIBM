import python_weather
import asyncio


async def get_weather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
    client = python_weather.Client(format=python_weather.METRIC)

    # fetch a weather forecast from a city
    weather = await client.find("Stuttgart")

    # returns the current day's forecast temperature (int)
    print(f"current weather for {weather.current.observation_point}: temp: {weather.current.temperature}, sky: {weather.current.sky_text}, humidity: {weather.current.humidity}, wind: {weather.current.wind_display}")
    # get the weather forecast for a few days
    for forecast in weather.forecasts:
        print(f"forecast date: {str(forecast.date)}, sky: {forecast.sky_text}, mean temp: {forecast.temperature}, low temp: {forecast.low}, high temp: {forecast.high}, precipitation value: {forecast.precip}")

    # close the wrapper once done
    await client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_weather())
