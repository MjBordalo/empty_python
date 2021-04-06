import os
import sys
from os import path
if sys.version_info[0] >= 3:
    import configparser
    VERSION = 3
else:
    VERSION = 2
    import ConfigParser as configparser

import versatile.python_aux_functions.github as github
import versatile.python_logger.my_logger as my_logger


cwd = os.getcwd()


'''
Server configs
'''
# config_file_name = '../cfg/params_server.cfg'
# if not path.isfile(config_file_name):
#     print("[Error] Current working folder is: "+ str(os.getcwd()))
#     print("[Error] Config for params lookingin: "+ str(config_file_name))
#     raise Exception("config file does not exits!")
#
# # setup to read config files
# config = configparser.ConfigParser()
# config.read(config_file_name)
# config.sections()


'''Logger'''
# logger_conf_filename = mqtt_params.CLIENTNAME + "/cfg/" + mqtt_params.CLIENTNAME + ".json"   #old organization
logger_conf_filename1 = cwd+"/../cfg/mqtt_logging.json"
logger_conf_filename2 = cwd+"/cfg/mqtt_logging.json"
if path.isfile(logger_conf_filename1):
    print("Going to load logger config file from: " + str(logger_conf_filename1))
    my_logger.setup_logging(default_path=logger_conf_filename1)

elif path.isfile(logger_conf_filename2):
    print("Going to load logger config file from: " + str(logger_conf_filename2))
    my_logger.setup_logging(default_path=logger_conf_filename2)
else:
    print("logger config file not defined, looking for: " +
          str(logger_conf_filename1) + " or :" + str(logger_conf_filename2))
    # logger_conf_filename = mqtt_params.CLIENTNAME + "/cfg/logging.json"
    my_logger.setup_logging()


main_logger = my_logger.logging.getLogger("mqtt_params")


'''Cfg file: Fetch topics. try to fetch mqtt params'''
conf_filename1 = "../cfg/mqtt.cfg"
conf_filename2 = "cfg/mqtt.cfg"
conf_filename = None
if path.isfile(conf_filename1):
    conf_filename = conf_filename1
elif path.isfile(conf_filename2):
    conf_filename = conf_filename2
else:
    main_logger.debug("Current working folder is: " + str(os.getcwd()))
    main_logger.debug("trying to get conf file: " + str(conf_filename))
    raise Exception("Specific config file does not exits! \n     This file should be in " +
                    conf_filename1 + " or in "+conf_filename2)

main_logger.debug("Loading .conf from " + conf_filename)

config = configparser.ConfigParser()
config.read(conf_filename)


'''
Mqtt topics
'''
'''
THIS CODE CANBE USED IF IN THE FUTURE WE WANT TO PUT ALL SERVERS IN THE SAME REPO
# Get name of mqtt client automatically

#Get name from folder name
main_name = path.abspath(sys.modules['__main__'].__file__)
# CLIENTNAME = main_name.split('/')[-2]
# print("Client Name is assumed to be: "+str(CLIENTNAME) +"    (got it from foldername)")

#get name from file name
CLIENTNAME = main_name.split('/')[-1].split("_")[0]
main_logger.info("Client Name is assumed to be: "+str(CLIENTNAME) +"    (got it from filename)")

conf_filename = str(CLIENTNAME)+'/cfg/'+str(CLIENTNAME)+'.cfg'
conf_filename2 = str(CLIENTNAME)+'/cfg/'+str(CLIENTNAME)+'.cfg'
'''

# python2 config["MQTT_TOPICS_SUB"]

MQTT_SUB_LIST = {}
MQTT_PUB_LIST = {}
MQTT_BROKER = {"address": "website", "port": 1883,
               "arg1": 60, "user": "website", "password": "psword"}
MQTT_KEEP_ALIVE = {}
CFG_BROKER = False

if VERSION == 2:
    '''mqtt subcribe topics'''
    list = config.options('MQTT_TOPICS_SUB')
    for t in list:
        MQTT_SUB_LIST[t] = {"topic": config.get('MQTT_TOPICS_SUB', t)}

    '''mqtt publish topics'''
    list = config.options('MQTT_TOPICS_PUB')
    for t in list:
        MQTT_PUB_LIST[t] = config.get('MQTT_TOPICS_PUB', t)

    ''' Try fetching broker configs'''
    try:
        list = config.options('MQTT_BROKER')
        for t in list:
            MQTT_BROKER[t] = config.get('MQTT_BROKER', t)
        main_logger.debug("Using cnf BROKER configs (from config file)")
        CFG_BROKER = True
    except:
        main_logger.debug(
            "Could not use broker config from conf file. Trying to use Repository config.")

    '''mqtt keep_alive topic'''
    try:
        list = config.options('MQTT_KEEP_ALIVE')
        for t in list:
            MQTT_KEEP_ALIVE[t] = config.get('MQTT_KEEP_ALIVE', t)
    except:
        main_logger.info("Could not use set_will from MQTT")

else:
    '''mqtt subcribe topics'''
    for t in config["MQTT_TOPICS_SUB"]:
        MQTT_SUB_LIST[t] = {"topic": config["MQTT_TOPICS_SUB"][t]}

    '''mqtt publish topics'''
    for t in config["MQTT_TOPICS_PUB"]:
        MQTT_PUB_LIST[t] = config["MQTT_TOPICS_PUB"][t]

    ''' mqtt broker settings'''
    try:
        for t in config["MQTT_BROKER"]:
            MQTT_BROKER[t] = config["MQTT_BROKER"][t]
        main_logger.debug("Using cnf BROKER configs (from config file)")
        CFG_BROKER = True
    except:
        main_logger.info(
            "Could not use broker config from conf file. Trying to use Repository config.")

    '''mqtt keep_alive topic'''
    try:
        for t in config["MQTT_KEEP_ALIVE"]:
            MQTT_KEEP_ALIVE[t] = config["MQTT_KEEP_ALIVE"][t]
    except:
        main_logger.info("Could not use set_will from MQTT")

'''
mqtt broker configs
'''
if not CFG_BROKER:
    try:
        AMBIENT = github.get_git_ambient(dir=cwd)
        success = True
    except:
        success = False
    if not success:
        try:
            AMBIENT = github.get_git_ambient(dir=cwd+"/..")
        except:
            main_logger.warning(
                "Could not use the git branch identification to set broker default setting. Considering DEV BROKER Settings.")
            AMBIENT = "DEVELOPMENT"

    if AMBIENT == "DEVELOPMENT":
        # MQTT_ADDR = "website"
        # MQTT_PORT = 1883
        # MQTT_ARG1 = 60
        MQTT_BROKER = {"address": "website", "port": 1883,
                       "arg1": 60, "user": "website", "password": "psword"}
    elif AMBIENT == "PRODUCTION":
        # TODO: UPDATE this when luis updates modifications on production (also update mqttclient.py - see todo)
        # MQTT_ADDR = "website"
        # MQTT_PORT = 1883
        # MQTT_ARG1 = 60
        # MQTT_BROKER = {"address":"website" , "port":1883,"arg1":60}
        MQTT_BROKER = {"address": "website", "port": 1883,
                       "arg1": 60, "user": "website", "password": "psword"}
    else:
        raise ("Git ambient not well defined!")

#############################################################

#############################################################
