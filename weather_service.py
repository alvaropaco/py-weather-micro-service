import os
import json
import sys

from urllib import quote
from nameko.rpc import rpc, RpcProxy
import requests

openweather_base_url = 'http://api.openweathermap.org/data/2.5/weather'
spotify_base_url = 'https://api.spotify.com/v1/'


def error(msg):
    raise Exception(msg)


def request(qstring, jwt):
    bearer = 'Bearer {}'.format(jwt)

    if jwt is None:
        return requests.request('GET', qstring)
    else:
        return requests.request(
            'GET', qstring, headers={
                'Authorization': bearer})


def get_playlists(weather, jwt):
    filtered = []

    if weather is None:
        error('Missing parameter')

    if weather['weather'] is None:
        error('Invalid location')

    main = weather['main']

    temperature = int(main['temp'])

    genrer = 'classical'

    if temperature > 30:
        genrer = 'party'
    elif temperature >= 15 and temperature <= 30:
        genrer = 'pop'
    elif temperature >= 10 and temperature <= 14:
        genrer = 'rock'

    current = weather['weather'][0]

    qstring = '{}search?seed_genres={}&q=name:{}&type=playlist'.format(
        spotify_base_url, genrer, current['description'])

    resp = request(qstring, jwt).json()

    if 'error' in resp:
        e = resp['error']
        error(e['message'])

    items = resp['playlists']['items']

    for playlist in items:
        filtered.append(playlist['name'])

    return filtered


def get_weather(args, appid):
    if 'city' not in args:
        if 'lat' not in args or 'lon' not in args:
            error('Missing parameter')
        else:
            r_str = '{}?units=metric&lat={}&lon={}&appid={}'.format(
                openweather_base_url, args['lat'], args['lon'], appid)
    else:
        r_str = '{}?units=metric&q={}&appid={}'.format(
            openweather_base_url, quote(
                args['city']), appid)
    print(r_str)
    resp = request(r_str, None)

    return resp.json()


class PlaylistsService:
    name = "playlists"

    zipcode_rpc = RpcProxy('playlistsservice')

    @rpc
    def get_playlists(self, appid, jwt, args):
        try:
            if args is None:
                error("Missing parameter")

            weather = get_weather(args, appid)

            if int(weather['cod']) != 200:
                return weather

            playlists = get_playlists(weather, jwt)

            return playlists
        except Exception as e:
            print str(e)
            sys.exit()
