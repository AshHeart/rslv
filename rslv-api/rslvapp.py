'''
    First endpoint for the REST API, the first file to be hit by the root url

    Initializes our Guinicorn Application and sets up the Flask REST Application
    that will deploy our models for real time usage

    Deployment is structured as follows

    URL("http://rslv.xyz/") -> Server(NGinx)(Proxy for rslv.xyz's IP) -> {Forwarded Request}Gunicorn(Pyhton Gateway) |
                                            App(Map Component){Forward Response} <- Server(Nginx){Forward Response} <-
'''

from flask import Flask, render_template
from predict_api import predict_api
import sys
import optparse
import time

app = Flask(__name__)

# Register other routes held in file:
# RSLV/predict_api.py
app.register_blueprint(predict_api)

start = int(round(time.time()))

# Home route for the url: "http://rslv.xyz/"
@app.route("/", methods=['GET'])
def index():

    return render_template('index.html')

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python simpleapp.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()

    if args.port == None:
        print("Missing required argument: -p/--port")
        sys.exit(1)

    app.run(host='0.0.0.0', port=int(args.port), debug=False)

# EOF