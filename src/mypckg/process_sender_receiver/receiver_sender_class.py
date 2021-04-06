import multiprocessing as mp
import sys

# fancy way to say that I am overriding something. It will print error if I am overriding something that I cannot override
def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

class ReceiverSender(mp.Process):
    instance = None

    @classmethod
    def create(cls, process_name="ReceiverSender",queue_send=None, queue_receive=None): #pensar em mais parametros
        """Create this class with defined parameters.

        """
        cls.instance = cls(process_name, queue_send, queue_receive)
        return cls.instance

    @classmethod
    def get(cls):
        """Retrieve this class's instance. Use .get to execute Class methods

        """
        return cls.instance

    @classmethod
    def get_message(cls):
        """Get a message that was sended by the ReceiverSender class.

        """
        rp = cls.get()
        try:
            message = rp.queue_send.get_nowait()
        except Exception:
            return None

        return message

    @classmethod
    def put_message(cls, message):
        """Send a message to the ReceiverSender class, so it will go to queue_receive
        
        """
        rp = cls.get()
        rp.queue_receive.put(message)

    def __init__(self, process_name, queue_send, queue_receive):
        """Initialize class 

        """
        self.debug = False
        mp.Process.__init__(self, name=process_name)
        
        self.exit = mp.Event()
        
        if queue_send is None:
            self.queue_send = mp.Queue()
        else:
            self.queue_send = queue_send
        
        if queue_receive is None:
            self.queue_receive = mp.Queue()
        else:
            self.queue_receive = queue_receive
        
    def initialize(self):
        """
            Function used inside intialize to use the info you inserted
        """
        pass    
            
    def introduction_function(self):
        """
            Function used before entering while loop 
        """
        pass

    def execute_message_received(self, message_received):
        """
            Function used to interpret messages from other modules 
        """
        pass
    
    def development_function(self):
        """
            Function used to be called inside while loop
            It must return something, and must return None to break from while loop
        """    
        return None

    def conclusion_function(self):
        """
            Function used after while loop break
        """
        pass      
        
    def queue_receive_error_handler(self, e):
        if type(e).__name__ != "Empty":
            print('ReceiverSender error, Error on line {} ... type: {} ... arg e: {}'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))    

    def run(self):
        """
            Generic way to use this class
        """

        self.introduction_function()

        while True:
            try:
                message_received = self.queue_receive.get_nowait()
            except Exception as e:
                self.queue_receive_error_handler(e)
            else:
                self.execute_message_received(message_received)

            if self.development_function() is None:
                break

        self.conclusion_function()        