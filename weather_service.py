from nameko.rpc import rpc

class WaetherService:
    name = "weather_service"

    @rpc
    def hello(self, name):
        return "Hello, {}!".format(name)