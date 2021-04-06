'''
Use rotating file handler in production
If you use FileHandler for writing logs, the size of log file will grow with time. Someday, it will occupy all of your disk. In order to avoid that situation, you should use RotatingFileHandler instead of FileHandler in production environment.

# source1: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
# source2: https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
# source3: https://docs.python.org/2/howto/logging.html#logging-advanced-tutorial


dependencies:
    pip install colorlog

how to use:
    1. make sure you have versatile branch correctly added to your project (see its README)
    2. on your project file add:
        import versatile.python_logger.my_logger as my_logger
    3. Create a loger object:
        my_logger.setup_logging()  #You only need to do this once on your entire project if y wont u can(and should) define  logger configuations by setting `default_path` and `default_level`
        main_logger = my_logger.logging.getLogger("mqtt_params")  # You can create multiple loggers with different names!
    4. Make sure you have a /log folder inside your project folder  #NOT NECESSARy ANYMORE
    5. Try it and enjoy the nice colours


@author: MiguelB
'''

import pprint
import json
import os
import logging
import logging.config
import colorlog  # source0: https://github.com/borntyping/python-colorlog
# The available color names are black, red, green, yellow, blue, purple, cyan and white.
from ..aux_functions.directories import create_dir_if_not_exists
print("Sucessfully imported my_logger")


HEADER_COLOR = '\033[95m'
OKBLUE_COLOR = '\033[94m'
OKGREEN_COLOR = '\033[92m'
WARNING_COLOR = '\033[93m'
FAIL_COLOR = '\033[91m'
ENDC_COLOR = '\033[0m'
BOLD_COLOR = '\033[1m'
UNDERLINE_COLOR = '\033[4m'


def setup_logging(
        default_path=None,
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    '''
    Setup logging configuration
    :param default_path: path to file with the log configs (see example on: ./logging.json)
    :param default_level: Setting to a certain Level all the Warnings until that level of severity will be displayed
            - Level	    Numeric value
            - CRITICAL	50
            - ERROR	    40
            - WARNING	30
            - INFO	    20
            - DEBUG	    10
            - NOTSET	0

            #NOTE This is only used if no path is found. Otherwise this should be set in the config file
    :param env_key: to connect to servers? see source1
    :return:
    '''
    """
    
    """
    if default_path is None:
        path = os.path.dirname(os.path.realpath(__file__)) + \
            "/logging.json"  # to fetch versatile
    else:
        path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        # make sure all log folder exists
        for h in config["handlers"]:
            if "filename" in config["handlers"][h]:
                log_dir = os.path.dirname(config["handlers"][h]["filename"])
                # print(log_dir)
                create_dir_if_not_exists(log_dir)

        logging.config.dictConfig(config)
        logging.info("Loaded logger config from file: "+str(path))
    else:
        logging.basicConfig(level=default_level)
        logging.warning(
            "Using default logger configs.\n    Could not read logger configs from: " + str(default_path))


def foo(string):
    print(string)


'''

Example on how to properly do exceptions:

  try:
    do_crazy_stuff
  except Exception:
    logger.exception("Print my personal msg. after this anice error message will be printed")

Example on how to change exception lvl:
 
  try:
    do_crazy_stuff
  except Exception:
    logger.warning("This error will be printed as a warning,but all error info will be printed", exc_info=True)
    
'''
