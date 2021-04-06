'''

dependencies:
pip install colorlog
'''



from .module1 import *
from versatile.python_logger.my_logger import *





if __name__ == "__main__":
    '''
    To try this module run this file  and this section will ran
    '''

    setup_logging(default_path="./Classes/logging.json")

    m1 = Module1Class(myname="M1")
    logging.info("Creating Module1")
    # m1.logger.debug("debug test")
    m1.print_info_msg_as_root_logger()
    m1.print_info_msg_as_instance_logger()
    m1.print_warning_msg()




    m2 = Module1Class(myname="Module2")
    logging.info("Creating Module2")
    # m1.logger.debug("debug test")
    m2.print_info_msg_as_root_logger()
    m2.print_info_msg_as_instance_logger()
    m2.print_error_msg()
    m2.zero_div()
    m2.logger.info("{}{}{}{}".format(BOLD_COLOR, HEADER_COLOR, ("*") * 20+ "EXAMPLE OF SPECIAL COLORED MESSAGE"+("*") * 20, ENDC_COLOR))
    m2.logger.info("{}{}{}".format( HEADER_COLOR, ("*") * 20+ "EXAMPLE OF SPECIAL COLORED MESSAGE not bold"+("*") * 20, ENDC_COLOR))
    m2.logger.info(HEADER_COLOR+ ("*") * 20+ "EXAMPLE OF SPECIAL COLORED MESSAGE not bold simpler writing"+("*") * 20)

