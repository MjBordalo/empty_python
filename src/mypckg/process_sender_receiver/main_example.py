"""
    This file receives info from the extension_example and sends back
"""

import extension_example


if __name__ == '__main__':
    cr = extension_example.CodeReader.create()    
    cr.daemon = True
    cr.start()


    while True:
        try:
            msg = cr.get_message()
            if msg is not None:
                print(msg)
                # This specific message will close the process. Doing cr.terminate() would terminate the process instantly.
                cr.put_message("THANK YOU!")
        except Exception as e:
            print("ERROR")

