# Playlists from Weather [![CircleCI](https://circleci.com/gh/alvaropaco/py-weather-micro-service.svg?style=svg)](https://circleci.com/gh/alvaropaco/py-weather-micro-service) [![Maintainability](https://api.codeclimate.com/v1/badges/3fc099559a53bc7800d0/maintainability)](https://codeclimate.com/github/alvaropaco/py-weather-micro-service/maintainability)

Tha main goal of this project is retreive a list of Spotify playlist based on current Weather. The Weather is retreived from the Open Weather Map service and filtered by *City* name or *geolocation* coordinates.

### Requeriments

* Docker I/O

### Building

Firstly we need to build the docker image:

`docker build -t ifood .` 

### Running

Run command will push up the micro-service:

`docker run -it -v $(pwd):/app -p 5000:5000  ifood ./entrypoint.sh` 

### Usage

Simple http call to the service URL:

`curl -X GET 127.0.0.1:5000/playlists?city=new+york -H "X-SPOTIFY-TOKEN: <spotify-jwt>" -H"X-OPENWM-APPID: 504002e265ed827f841600d3259c32ee"` 

### Testing 

Can run the API tests:

`docker run -it -v $(pwd):/app -p 5000:5000  ifood ./entrypoint.tests.sh`