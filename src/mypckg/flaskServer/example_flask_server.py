#!/usr/bin/python3

import time
from threading import Thread, Timer
import colorlog
import os
import datetime
import json
import importlib
import sys
import copy
from subprocess import call
import logging


import requests
from flask import Flask, render_template, redirect, request, url_for
import urllib3


FILE_LOG = "../example.log"
FLASK_PORT = 5000 # whatever
SOME_URL = "127.0.0.1:5002/update" # sends to another flask on same pc


class MQTT_Client(Thread):


    def __init__(self, name):

        Thread.__init__(self)
        self.name                       = name
        self.logger                     = self.getLogger()

        self.flaskServerSetup()


    def getLogger(self):

        """
        Defines and returns the logger for thread
        """

        # log definition
        logger = colorlog.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s [' + self.name + '] %(message)s')

        # file handler log

        fh = logging.FileHandler(FILE_LOG)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # create console handler
        ch = colorlog.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(asctime)s %(levelname)s   %(blue)s[' + self.name + ']%(reset)s  %(message)s',))
        logger.addHandler(ch)

        return logger


    def flaskServerSetup(self):

        """ 
        -----------------------
        FLASK SERVER SETUP  
        -----------------------
        """

        SERVER_ROUT = "../"   # to be changed
        
        # initiate flask app
        flask_server = Flask(__name__, template_folder=SERVER_ROUT)

        @flask_server.route('/update', methods = ['POST'])
        def update():
            if request.method == "POST":
                try:
                    new_data = request.get_json()

                    self.logger.info('Message: {}'.format(new_data))
                
                    # TO send something...

                    message = {"supercode": 1234}

                    encoded_message = json.dumps(message).encode('utf-8')
                    http    = urllib3.PoolManager()
                    req     = http.request('POST', SOME_URL, body=encoded_message, headers={'Content-Type':'application/json'})

                    return "SUCCESS"

                except Exception as e:
                    self.logger.warning('wb(): got POST with data not in the right format: {}'.format(e))
                    return "FAIL"

        def shutdown_server():

            """
            This method can be used for shutting down server safely.
            """
    
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @flask_server.after_request
        def add_headers(response):

            """
            This method gives access to post and get
            """

            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Methods','POST,GET')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            return response


        self.flask_server = flask_server



    def statesCycle(self):

        while True :

            self.logger.info('This cycle is for anything synchronous on program, though you have an asynchronous Flask server...')
            time.sleep(5)



    def run(self):

        some_cycle = Timer(1, self.some_cycle)
        some_cycle.start()

        self.logger.info('Will start FLASK SERVER.')

        self.flask_server.run(host='0.0.0.0',debug=False,port=FLASK_PORT)

            

########################
### USED FOR TESTING ###
########################
if __name__ == "__main__":

    FLASK = FlaskServer('FLASK')
    FLASK.start()