# Example MQTT client


import os
# In the example the mqtt_logger.json is configured to right the logs to ./log folder. So to avoid errors on can make sure the path exists
# a common alternative is ../log. This should be runned before importing some versatile applications
if not os.path.exists("./log"):
    os.mkdir("./log")


from versatile.python_mqttServer.mqttclient import *
from versatile.python_aux_functions.python_version import VERSION

'''Here is an example on how to use versatile.python_mqttServer.mqttclient

NOTE: this document should not be run in this file. follow the instructions in the versatile/python_mqttServer/README.md
'''


class Client(MqttClient):
    def __init__(self):
        for key in mqtt_params.MQTT_SUB_LIST:
            mqtt_params.MQTT_SUB_LIST[key]["method_link"] = getattr(Client, "on_message_" + key)
        if VERSION == 3:
            super().__init__()
        elif VERSION == 2:
            super(Client, self).__init__()

    '''Example of a callback defenition after on_message the remaining part of the function should be the same
    as in the .cfg folder under the section of [MQTT_TOPICS_SUB]'''

    @staticmethod
    def on_message_report(client, data, message):
        """
            :param client:
            :param data:
            :param message:
        """
        try:
            MqttClient.on_message(client, data, message)
            topic = message.topic
            root_topic = topic.split("/")[0]
            # serial of the gateway
            gateway = topic.split("/")[1]
            payload = json.loads(message.payload.decode("utf-8"))

            Client.main_logger.info("This is just an example on message report. \n                             "
                                    "Going to do a publish for fun.")

            '''How to publish'''
            Client.add_msg_queue("EMEL", "randSerial", mqtt_params.MQTT_PUB_LIST['pub_example'],
                                 "my random publish message", retained = False)
            # Note: on message: (in this case: "my random publish message") sometime we send json.dump() . in this case on the subscriber side you should make sure a json.loads() is called

        except Exception:
            MqttClient.main_logger.exception("Exception")

# running the thread
if __name__ == "__main__":
    DAEMON = Client()
    DAEMON.start()
