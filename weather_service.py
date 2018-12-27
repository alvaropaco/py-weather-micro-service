from nameko.rpc import rpc


def getWeather(self, qstring):
    return "Hello, {}!".format(qstring)


class WaetherService:
    name = "weather_service"

    @rpc
    def getPlaylists(self, city, lat, long):
        return "Hello, {}!".format()
