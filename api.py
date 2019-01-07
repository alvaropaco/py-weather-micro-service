from flask import Flask, request, jsonify
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost:5672"}


@app.route('/playlists', methods=['GET'])
def playlists():
    """
    Micro Service Based Compute and Mail API
    This API is made with Flask, Flasgger and Nameko
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
      openwm_appid  = request.headers.get('X-OPENWM-APPID')
      spotify_token = request.headers.get('X-SPOTIFY-TOKEN')
      
      result = rpc.playlists.get_playlists(
          openwm_appid, spotify_token, request.args)
      return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
