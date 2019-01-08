import os
import json
import sys

from urllib import quote
from nameko.rpc import rpc, RpcProxy
import requests

openweather_base_url = 'http://api.openweathermap.org/data/2.5/weather'
spotify_base_url = 'https://api.spotify.com/v1/'


def error(msg):
    """Return a Exception object

    This function is a reuse function to handle exceptions
    """
    raise Exception(msg)


def request(qstring, jwt):
    """
    Return the result from a Request
    """
    bearer = 'Bearer {}'.format(jwt)

    # JWT necessary to the Spotify Authorization
    if jwt is None:
        return requests.request('GET', qstring)
    else:
        # If is not a Spotify call
        return requests.request(
            'GET', qstring, headers={
                'Authorization': bearer})


def get_playlists(weather, jwt):
    """ Return a list of Spotify playlists

    From a Weather predict, we consult the
    Spotify API to return results based on the
    weather description.
    """

    filtered = []

    if weather is None:
        error('Missing parameter')

    if weather['weather'] is None:
        error('Invalid location')

    # Main attributte contains the temperature meassure
    main = weather['main']

    # Convert string to int
    temperature = int(main['temp'])

    # Default Genre
    genre = 'classical'

    # If temperature (celcius) is above 30 degrees, suggest tracks for party
    # In case temperature is between 15 and 30 degrees, suggest pop music tracks
    # If it's a bit chilly (between 10 and 14 degrees), suggest rock music tracks
    # Otherwise, if it's freezing outside, suggests classical music tracks
    if temperature > 30:
        genre = 'party'
    elif temperature >= 15 and temperature <= 30:
        genre = 'pop'
    elif temperature >= 10 and temperature <= 14:
        genre = 'rock'

    # Get current weather to check temperatury
    current = weather['weather'][0]

    qstring = '{}search?q=name:{}&type=playlist'.format(
        spotify_base_url, quote(current['description']))

    resp = request(qstring, jwt).json()

    # Is receives nothing
    if 'error' in resp:
        e = resp['error']
        error(e['message'])

    # getting plalists itens
    items = resp['playlists']['items']

    # Build the list of the names
    for playlist in items:
        filtered.append(playlist['name'])

    return filtered


def get_weather(args, appid):
    """Return a Weather object

    This call consumes the open Weather Map API to retreive the weather information about some geographi coordinate or city name.
    """

    # Check if seach by City
    if 'city' not in args:
        # Check if search by coordinates
        if 'lat' not in args or 'lon' not in args:
            error('Missing parameter')
        else:
            # Query string to coordinates
            r_str = '{}?units=metric&lat={}&lon={}&appid={}'.format(
                openweather_base_url, args['lat'], args['lon'], appid)
    else:
        # Query string to City
        r_str = '{}?units=metric&q={}&appid={}'.format(
            openweather_base_url, quote(
                args['city']), appid)

    # Requesting the API
    resp = request(r_str, None)

    # Returns a JSON object
    return resp.json()


class PlaylistsService:
    """Playlists Srevice

    Returns:
        list: A list of playlists
    """

    name = "playlists"

    zipcode_rpc = RpcProxy('playlistsservice')

    @rpc
    def get_playlists(self, appid, jwt, args):
        """[summary]

        Arguments:
            appid (string): Open Weather Map AppID
            jwt   (string): Spotify Authorization Token
            args    (dict): A Dict (city, lat, long)

        Returns:
            list: A list of playlists
        """
        try:
            # Check if is passed args
            if args is None:
                error("Missing parameter")

            # Consuming the OWM API
            weather = get_weather(args, appid)

            # Check response
            if int(weather['cod']) != 200:
                return weather

            # Consuming Spotify API
            playlists = get_playlists(weather, jwt)

            return playlists
        except Exception as e:
            return str({'Error': str(e)})
