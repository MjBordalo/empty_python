'''

'''

from versatile.python_logger.my_logger import *


class Module1Class():


    def __init__(self,myname=__name__):
        self.logger = logging.getLogger(myname)

    def print_info_msg_as_root_logger(self):
        logging.info("This is just a normal message of type INFO sent as root name")

    def print_info_msg_as_instance_logger(self):
        self.logger.info("This is just a normal message of type INFO sent with the instance name")


    def print_error_msg(self):
        self.logger.error("This is an error")

    def print_warning_msg(self):
        self.logger.warning("This is a warning")

    def zero_div(self):
        try:
            1/0
        except ZeroDivisionError:
            self.logger.exception("There was a zero devision ")
        except Exception as e:
            self.logger.exception("There was an unknown error")



if __name__ == "__main__":
    '''
    To try this module run this file  and this section will ran
    '''

    setup_logging(default_path="./Classes/logging.json")
    logging.info("Creating Module1")

    m1= Module1Class()
    # m1.logger.debug("debug test")
    m1.print_info_msg()