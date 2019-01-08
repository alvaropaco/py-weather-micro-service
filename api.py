from flask import Flask, request, jsonify
from nameko.standalone.rpc import ClusterRpcProxy

CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost:5672"}
app = Flask(__name__)


@app.route('/playlists', methods=['GET'])
def playlists():
    """
    Micro Service Based Weather and Spotify API
    This API is made with Flask and Nameko
    ---
    parameters:
      - name: zipcode
        in: path
        required: true
        schema:
          type: integer
        description: location ZipCode
    responses:
      200:
        description: Location data
    """
    with ClusterRpcProxy(CONFIG) as rpc:
        # Get the Spotify Authrization Token from header
        # and OWM AppId from the header
        openwm_appid = request.headers.get('X-OPENWM-APPID')
        spotify_token = request.headers.get('X-SPOTIFY-TOKEN')

        # Consuming Nameko service
        # Here we pass the OpenWeatherMap AppId
        # and the Spotify JWT
        result = rpc.playlists.get_playlists(
            openwm_appid, spotify_token, request.args)
        return jsonify(result), 200


if __name__ == "__main__":
    """Start Flask app to serve mircoservices"""
    app.run(host='0.0.0.0')
