#!/usr/bin/env python
"""Push bullet API

Allows to easily send notification to a computer or android device.
Thread implementation allows to work simultaneous with other project without waiting for file uploads

source:
    * https://github.com/rbrcsk/pushbullet.py
dependencies:
    * pip install pushbullet.py
"""
__author__ = "Miguel Bordalo"
__version__ = "0.1"
__email__ = "miguel.b.fernandes@gmail.com"
__status__ = "master"


from pushbullet import Pushbullet
import os
from queue import Queue
from threading import Thread
import time as tm


import socket


class PushBulletAPI(Thread):
    '''
    api_key has to be get from https://www.pushbullet.com/#settings/account
    Note:
    in the __init_ one can specify the channel that wants the communication to
    go and all comunitcations will go directly to that channel: No need to
    specify in the queue_push_text and queue_push_file functions the channel
    '''

    def __init__(self, api_key, channel_tag=None):

        Thread.__init__(self)
        self.pb = Pushbullet(api_key)

        self.text_queue = Queue()
        self.file_queue = Queue()
        self._mystop = False

        if channel_tag is not None:
            try:
                self.channel = self.get_channel(channel_tag)
            except:
                print("[ERROR] Could not load PushBullet channel:  " +
                      str(channel_tag))
                self.channel = None
        else:
            self.channel = None

    def queue_push_text(self, body, title=socket.gethostname(), channel=None):
        if self.channel is not None and channel is None:
            channel = self.channel
        self.text_queue.put({"title": title, "body": body, "channel": channel})

    def queue_push_file(self, filename, channel=None):
        if self.channel is not None and channel is None:
            channel = self.channel
        self.file_queue.put({"filename": filename, "channel": channel})

    def _push_text(self, title, body, channel=None):
        if channel is None:
            return self.pb.push_note(title, body)
        else:
            return self.pb.push_note(title, body, channel=channel)

    def _push_link(self, title, body, channel=None):
        if channel is None:
            return self.pb.push_note(title, body)
        else:
            return self.pb.push_note(title, body, channel=channel)

    def _push_file(self, filename, channel=None):
        path, fn = os.path.split(filename)
        with open(filename, "rb") as pic:
            file_data = self.pb.upload_file(pic, fn)

        if channel is None:
            return self.pb.push_file(**file_data)
        else:
            return self.pb.push_file(**file_data, channel=channel)

    def get_all_channels(self):
        return self.pb.channels

    def get_channel(self, channel_name):
        return self.pb.get_channel(channel_name)

    def mystop(self):
        self._mystop = True

    def run(self):
        while not self._mystop or not self.text_queue.empty() or not self.file_queue.empty():
            while not self.text_queue.empty():
                item = self.text_queue.get()
                self._push_text(item["title"], item["body"],
                                channel=item["channel"])

            while not self.file_queue.empty():
                item = self.file_queue.get()
                self._push_file(item["filename"], channel=item["channel"])

            tm.sleep(1)


# test me:
if __name__ == "__main__":
    api_key = "o.pXSZkAUvnbmlwsKPFc0PSLCTDYhTpfua"
    PB = PushBulletAPI(api_key)
    PB.start()

    # PB.push_text("mytitle","my beautiful text")
    print(PB.get_all_channels())
    FS_channel = PB.get_channel("firespot")
    # PB.push_text("mytitle","my beautiful text", channel=FS_channel )
    file_name = "/home/mjbordalo/Figure_1.png"
    # PB.push_file(file_name, channel=FS_channel)
    PB.queue_push_file(file_name, channel=FS_channel)
    PB.mystop()
