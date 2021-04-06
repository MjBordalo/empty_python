#!/usr/bin/python3
"""
A MQTT server that's responsible for
the communication between local controllers
and the web application

@author: MiguelB
"""
from ..python_aux_functions.python_version import VERSION
import time
import sys
if VERSION == 3:
    import queue
else:
    import Queue as queue

import time as tm
import json
from threading import Thread
import paho.mqtt.client as mqtt
from datetime import datetime
from os import path

# import mqtt_params
# from versatile.python_mqttServer import mqtt_params
from . import mqtt_params as mqtt_params
# import versatile.python_logger.my_logger as my_logger
from ..python_logger import my_logger


class MqttClient(Thread):
    """
    class that functions as a server
    with mqtt protocol implemented
    for communication
        :param Thread:
    """

    '''queue with the messages to be sent to controllers'''
    message_queue = queue.Queue()
    send_config_flag = False

    '''Logger'''
    main_logger = my_logger.logging.getLogger("MQTT")

    def __init__(self):
        Thread.__init__(self)
        mqtt.Client.connected_flag = False
        # Trying to have information when no connection is established
        MqttClient.connected_flag = mqtt.Client.connected_flag
        # self.connection = mqtt.Client(client_id="", clean_session=True)

        # After luis made modification
        # TODO: TODO: UPDATE this when luis updates modifications on production
        # custom_headers = {"Authorization": "basic websit"}
        while True:
            try:
                if "user" in mqtt_params.MQTT_BROKER and "password" in mqtt_params.MQTT_BROKER:
                    self.connection = mqtt.Client(
                        clean_session=True, transport="tcp")
                    self.connection.username_pw_set(
                        mqtt_params.MQTT_BROKER["user"], password=mqtt_params.MQTT_BROKER["password"])
                else:
                    self.connection = mqtt.Client(clean_session=True)

                ''' Add all the callback functions associated to a certain topic'''
                for key in mqtt_params.MQTT_SUB_LIST:
                    self.connection.message_callback_add(mqtt_params.MQTT_SUB_LIST[key]["topic"],
                                                         mqtt_params.MQTT_SUB_LIST[key]["method_link"])

                '''bind functions to callbacks'''
                if "payload" in mqtt_params.MQTT_KEEP_ALIVE and "topic" in mqtt_params.MQTT_KEEP_ALIVE:
                    topic = mqtt_params.MQTT_KEEP_ALIVE["topic"]
                    payload = mqtt_params.MQTT_KEEP_ALIVE["payload"]
                    MqttClient.main_logger.info(
                        "I am using set_will --> topic: {} , payload: {}".format(topic, payload))
                    self.connection.will_set(
                        topic, payload=payload, qos=2, retain=True)

                self.connection.on_disconnect = self.on_disconnect
                self.connection.on_connect = self.on_connect
                self.connection.on_message = self.on_message
                self.connection.on_publish = self.on_publish
                self.connection.on_subscribe = self.on_subscribe

                self.MQTT_SUB_LIST = mqtt_params.MQTT_SUB_LIST
                self.MQTT_PUB_LIST = mqtt_params.MQTT_PUB_LIST

                self.stop_ = False
            except Exception as e:
                MqttClient.main_logger.info(
                    "No internet connection Waiting 5 seconds for next try. Error: {} ".format(e))
                time.sleep(5)
            else:
                break

    @staticmethod
    def on_disconnect(client, data, rc):
        if rc != 0:
            client.connected_flag = False
            MqttClient.connected_flag = client.connected_flag
            msg = "[mqtt client] ERROR - Bad connection; Returned code = %i @ %s" % (
                rc, datetime.now().strftime("%H:%M:%S.%f %d-%m-%Y"))
            MqttClient.main_logger.info(msg)

    @staticmethod
    def on_connect(client, data, flags, rc):
        """
        method from mqtt displays a message
        when connection is established
            :param client:
            :param data:
            :param flags:
            :param rc:
        """
        if rc == 0:
            client.connected_flag = True
            msg = "[mqtt client] OK - connected successfully @ " + \
                datetime.now().strftime("%H:%M:%S.%f %d-%m-%Y")
            for key in mqtt_params.MQTT_SUB_LIST:
                client.subscribe(mqtt_params.MQTT_SUB_LIST[key]["topic"], 2)
        else:
            client.connected_flag = False
            msg = "[mqtt client] ERROR - Bad connection; Returned code = %i @ %s" % (
                rc, datetime.now().strftime("%H:%M:%S.%f %d-%m-%Y"))
        MqttClient.connected_flag = client.connected_flag
        MqttClient.main_logger.info(msg)

    @staticmethod
    def on_message(client, data, message):
        """
        display feedback when receveing a message
            :param client:
            :param data:
            :param message:
        """
        # MqttClient.main_logger.debug("From topic: " + str(message.topic)+" :: received: "+ str(message.payload.decode("utf-8")) + " type:" + str(type(message.payload)))
        pass

    @staticmethod
    def on_publish(client, data, mid):
        """
        on publish feedback
            :param client:
            :param data:
            :param mid:
        """
        # MqttClient.main_logger.debug("published #" + str(mid) + " :" + str(client._current_out_packet['packet'][5:].decode("utf-8")))
        pass

    @staticmethod
    def on_subscribe(client, data, mid, granted_qos):
        """
        on subscribe topic feedback
            :param client:
            :param data:
            :param mid:
            :param granted_qos:
        """
        MqttClient.main_logger.info(
            "[mqtt client] subscribed topic: (msg id)-%s qos-%s data-%s" % (str(mid), str(granted_qos), str(data)))
        pass

    @staticmethod
    def add_msg_queue(gateway, serial, subtopic, msg, retain=False, qos=2):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        return MqttClient.message_queue.put({"topic": str(gateway)+"/"+str(serial)+subtopic, "msg": msg, "retain": retain, "qos": qos})

    @staticmethod
    def add_msg_queue_full_topic(topic, msg, retain=False, qos=2):
        if isinstance(msg, dict):
            msg = json.dumps(msg)
        return MqttClient.message_queue.put(
            {"topic": str(topic), "msg": msg, "retain": retain, "qos": qos})
    ####################CALLBACK FUNCTION EXAMPLE####################

    def stop(self):
        self.stop_ = True

    def run(self):

        while True:
            try:
                # handle the connection
                # NOTE: these configs are automatically set to dev or production depending on github branch
                MqttClient.main_logger.info("[mqtt client] Connecting to broker " + mqtt_params.MQTT_BROKER["address"] + ":" + str(
                    mqtt_params.MQTT_BROKER["port"]))
                # threaded loop which handles reconnect alone
                self.connection.loop_start()
                self.connection.connect(mqtt_params.MQTT_BROKER["address"], int(
                    mqtt_params.MQTT_BROKER["port"]), int(mqtt_params.MQTT_BROKER["arg1"]))

                while self.connection.connected_flag is not True:
                    MqttClient.main_logger.info("[mqtt client] attempting...")
                    tm.sleep(1)

                '''Subscribe to topics'''
                for key in mqtt_params.MQTT_SUB_LIST:
                    self.connection.subscribe(
                        mqtt_params.MQTT_SUB_LIST[key]["topic"], 1)
                    MqttClient.main_logger.info(
                        "Subscribing to: " + str(mqtt_params.MQTT_SUB_LIST[key]["topic"]))

            except Exception as e:
                MqttClient.main_logger.info(
                    "No internet connection Waiting 5 secs for next try {}. Error: ".format(e))
                time.sleep(5)
            else:
                break

        while not self.stop_:
            while not MqttClient.message_queue.empty():
                connected_flag = MqttClient.connected_flag
                if connected_flag is True:
                    msg = MqttClient.message_queue.get()
                    if "qos" in msg:
                        qos = msg["qos"]
                    else:
                        qos = 2
                    self.connection.publish(
                        msg["topic"], msg["msg"], retain=msg["retain"], qos=qos)
                else:
                    time.sleep(5)

            tm.sleep(1)
