# Playlists from Weather

Tha main goal of this project is retreive a list of Spotify playlist based on current Weather. The Weather is retreived from the Open Weather Map service and filtered by *City* name or *geolocation* coordinates.

### Requeriments

* Docker I/O

### Installation

`docker build -t ifood .` 

### Usage

`docker run -it -p 5000:5000 ifood ./entrypoint.sh` 