# How to Run a new mqtt Client or Server

 1. Check the example on  versatile/python_mqttServer/mqttclient/example-application-server
 2. Copy example-application-server folder and rename it to CLIENTNAME (I suggest: myprojectname-application-server) (this folder should be on the same folder as versatile : see hierarchy at the end)
 3. Rename the example-application-server_client.py to CLIENTNAME_client.py
 4. Edit mqtt.cfg : this file define the topics you would like to subscribe under [MQTT_TOPICS_SUB] this is
done automatically. e.g.: report=EXAMPLE/+/report
 4. This topics will be automatically subscribed. On your myprojectname-application-server.py and inside the class Create the functions that should be run when a message is send via this topic. Make sure the function starts with 'on_message' and finished as you defined in .cfg . In this case on_message_report. check on_message_report() example.
 4. Add the publish topics under [MQTT_TOPICS_PUB]. to publish check example on myprojectname-application-server.py file in '''How to publish''' (line 50)
 5. edit CLIENTNAME.json content and change where you see "example-application-server" to your CLIENTNAME  (TODO: THIS SHOULD BE IMPROVED)
 6. Make sure there is a `log`  folder inside your project folder
 7. cd to /src and run it as a package: ` python3 -m CLIENTNAME.CLIENTNAME_client` example: `python3 -m example-application-server.example-application-server_client`

Optional:
  * If you want to manually define a different broker than the common used in DEV and PRODUCTION. Then you can set in the .cfg file the section [MQTT_BROKER] with the fields: address,port, and arg1=60. If needed you can also specify user and password.

hierarchy example:
 ```
  \my_project_name
    \cfg
      \mqtt.cfg
    \log
    \src
         \versatile  (Do not copy this folder! plz check versatile README on how to import a submodule branch so you can keep it updated)
         \myprojectname-application-server   (copy this folder from example-application-server)
             \myprojectname-application-server-client.py

 ```
