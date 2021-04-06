import logging
import logging.handlers
import io, json, os, sys
from os import path as op
from datetime import datetime
from functools import reduce

class Manager():

    @staticmethod
    def create_folder(folder_name):
        if not op.exists(folder_name):
            os.makedirs(folder_name)
        else:
            return False    

    def write_file(self, path, message):
        try:
            with io.open(path, 'w') as  f:
                json.dump(message, f)
        except Exception as e:
            self.error_message("Error due--> path: {} and message: {} ".format(path, message), e)
        else:
            return True    

    def read_file(self, path):        
        try:
            with io.open(path, 'r') as f:
                value = json.load(f) 
        except Exception as e:
            self.error_message(e, "ERROR OPEN: {}".format(path))
            value = None
        return value
        
    
    def error_message(self, txt_error, error):
        if self.logger is None:
            print('{}:, Error on line {}, TYPE: {}, ARGS: {}'.format(txt_error, sys.exc_info()[-1].tb_lineno, type(error).__name__, error))
        else:
            self.logger.error('{}:, Error on line {}, TYPE: {}, ARGS: {}'.format(txt_error, sys.exc_info()[-1].tb_lineno, type(error).__name__, error))

    def queue_receive_error_handler(self, e, text):
        if type(e).__name__ != "Empty":
            if self.logger is None:
                print('{}, Error on line {} ... type: {} ... arg e: {}'.format(text,sys.exc_info()[-1].tb_lineno, type(e).__name__, e))
            else:    
                self.logger.error('{}, Error on line {} ... type: {} ... arg e: {}'.format(text,sys.exc_info()[-1].tb_lineno, type(e).__name__, e))        

    def unexpected_passage(self, text):
        if self.logger is None:
            print('UNEXPECTED_PASSAGE: {}'.format(text))        
        else:
            self.logger.fatal('UNEXPECTED_PASSAGE: {}'.format(text))        

    def debug_message(self, message, where):
        if self.logger is None:
            print("In function: {} got: {}".format(where, message))
        else:
            self.logger.debug("In function: {} got: {}".format(where, message))

    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.logger = None

    def create_logger(self, log_dir=None, filename=None, level=logging.DEBUG, when='midnight', interval=1, backupCount=7):
        name = self.logger_name
        """Initialize self.logger 

        :param filename: the name of the file
        :param_type filename: str or None
        :param int level: the logging Level
        :param str when: the time to rotate
        :param int interval: the interval days to rotate 
        :param int backupCount: the number of files to keep

        """
        if log_dir is None:
            self.log_dir = op.abspath(op.join(op.dirname(__file__), '..', 'logs'))
        else:
            self.log_dir=log_dir    
        Manager.create_folder(self.log_dir)

        # Determine the log filename.  It is either supplied or computed.
        log_filename = '{0}.log'.format(name)
        filename = filename or op.join(self.log_dir, log_filename)

        formatter = logging.Formatter('%(asctime)s;%(message)s',
                                    '%Y-%m-%d %H:%M:%S')

        # Set up the logging handler.  Rotate the logs everyday at
        # midnight, and keep the last 7.
        handler = logging.handlers.TimedRotatingFileHandler(filename,
                                                            when=when,
                                                            interval=interval,
                                                            backupCount=backupCount)
        handler.setFormatter(formatter)

        # Create and return the logger.
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        self.logger = logger

    def create_cascade_logs(self, start_folder, message, **kargs):
        """
        if it is python version less than 3.6.0 it will have alphabetical order DESC
        example usage: (start_folder_path, message, first_folder_name=('a'), second_folder_name=('b'), third_folder_name=('c', 'c'), forth_folder_name=('d', 'b', 'a')) 
        start_folder_path: is a string with log folder path example: "/bla/bla/blabla"
        message: dictionary with nested dictionary
        kargs: cascade folder name

        :return: last_folder_path
        """

        import sys

        version_str = sys.version[0:5]
        if not (version_str[0] == '3' and int(version_str[2]) >= 6):
            import collections
            ord_dict = collections.OrderedDict()
            for key, value in sorted(kargs.items(), reverse=True):
                ord_dict[key] = value

            kargs = ord_dict
        
        Manager.create_folder(start_folder)
        next_folder = start_folder
        for key in kargs:
            try:
                value = reduce(dict.get, kargs[key], message)
            except Exception as e:
                self.error_message("key path: {} doesn't exist in message: {}".format(kargs[key], message), e)
                return None
            else:
                if value is not None:
                    next_folder = next_folder + "/" + str(value)
                    Manager.create_folder(next_folder)
                

        now = datetime.now()
        filename = "log-{}.txt".format(now.date())
        file_path = next_folder + "/" + filename
        with open(file_path, "a") as f:
            try:
                json.dump(message, f)
                f.write("\n")    
            except Exception as e:
                self.error_message("error appending file: {}".format(file_path), e)



    def read_log(self, filename):
        """Read the named log and return it's contents.
        :param str filename: the name of the log
        :return: the log contents or None
        :rtype: str or None
        """

        fname = op.join(self.log_dir, filename)
        txt = []
        if op.exists(fname):
            with open(fname, "r") as f:
                for line in f:
                    txt.append(line)
                return txt
        else:
            return None


def test():
    t_l = Manager("test")
    t_l.create_logger()
    t_l.logger.info("MORRE")

if __name__ == "__main__":
    test()
