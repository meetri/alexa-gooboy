import sys
import socket
import json
from urlparse import urlparse
from flask import Flask,render_template,request

sys.path.append("./helpers" )

import alexa

app = Flask (__name__)

@app.route("/", methods = ['GET','POST'])
def main():

    #output = '<speak>Gooboy says, <audio src="https://echo.enochclock.com/static/nicetomeetyou.mp3" /></speak>'

    # https://bonsai.io/clusters/first-cluster-2762909896/console
    gooboy = alexa.Gooboy(["https://77hw45ajnp:4m7fx1brse@first-cluster-2762909896.us-east-1.bonsaisearch.net"],"gooboy")

    if len(request.data) > 0:
        indata = json.loads ( request.data )
        if "request" in indata and "intent" in indata["request"]:
            gooboy.process_intent ( indata["request"]["intent"] )

    resp = gooboy.build_response()
    return json.dumps ( resp )

