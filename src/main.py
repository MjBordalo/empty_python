#!/usr/bin/env python
""" Main empty python project

Helps to create a new python project

source:
    * 
dependencies:
    * pip install colorlog
"""
__author__ = "Miguel Bordalo"
__version__ = "0.1"
__email__ = "miguel.b.fernandes@gmail.com"
__status__ = "master"


import module1
from mypckg.logger.my_logger import *


if __name__ == "__main__":
    '''
    To try this module run this file  and this section will ran
    '''

    setup_logging(default_path="../cfg/logging.json")

    m1 = module1.ModuleClass(myname="M1")
    logging.info("Creating Module1.")
    # m1.logger.debug("debug test")
    m1.print_info_msg_as_root_logger()
    m1.print_info_msg_as_instance_logger()
    m1.print_warning_msg()

    # Example on creating a logger with a different name
    logger = logging.getLogger("main")
    logger.debug(
        "I just created a new root loger but changed it name to main. And this is a debug lvl message")

    # Example on creating another instance of moduleClass
    m2 = module1.ModuleClass(myname="Module2")
    logging.info("Creating Module2")
    m2.print_info_msg_as_instance_logger()
    m2.print_error_msg()
    m2.zero_div()
    m2.logger.info("{}{}{}{}".format(BOLD_COLOR, HEADER_COLOR, ("*") *
                   20 + "EXAMPLE OF SPECIAL COLORED MESSAGE"+("*") * 20, ENDC_COLOR))
    m2.logger.info("{}{}{}".format(HEADER_COLOR, ("*") * 20 +
                   "EXAMPLE OF SPECIAL COLORED MESSAGE not bold"+("*") * 20, ENDC_COLOR))
    m2.logger.info(HEADER_COLOR + ("*") * 20 +
                   "EXAMPLE OF SPECIAL COLORED MESSAGE not bold simpler writing"+("*") * 20)
