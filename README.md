# Playlists from Weather

Tha main goal of this project is retreive a list of Spotify playlist based on current Weather. The Weather is retreived from the Open Weather Map service and filtered by *City* name or *geolocation* coordinates.

### Requeriments

* Docker I/O

### Building

`docker build -t ifood .` 

### Running

`docker run -it -v $(pwd):/app -p 5000:5000  ifood ./entrypoint.sh` 

### Usage

`curl -X GET 127.0.0.1:5000/playlists?city=new+york -H "X-SPOTIFY-TOKEN: <spotify-jwt>" -H"X-OPENWM-APPID: 504002e265ed827f841600d3259c32ee"` 

### Testing 

`docker run -it -v $(pwd):/app -p 5000:5000  ifood ./entrypoint.tests.sh`