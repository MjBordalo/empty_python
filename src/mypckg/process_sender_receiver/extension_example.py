"""
	This file is an example of a posible way to extende the ReceiverSender class.
	It implements an easy code_reader (bar_code, qr_code, etc...)
"""


import sys

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

from receiver_sender_class import ReceiverSender, overrides


class CodeReader(ReceiverSender):
	instance = None

	# This is expected to be like this. 
	def __init__(self, process_name="CodeReader", queue_send=None, queue_receive=None):
		super().__init__(process_name, queue_send, queue_receive)
	
	
	
		# placing @overrides(ReceiverSender) will get you an error since this method is not in ReceiverSender class.
	def decode(self, image):
		decodedObjects = pyzbar.decode(image)
 
	  # Print results
		if self.debug is True:
			for obj in decodedObjects:
				print('Type : ', obj.type)
				print('Data : ', obj.data,'\n')

		return decodedObjects 

	@overrides(ReceiverSender)
	def introduction_function(self):
		# I only have one cam so just find the first good id
		cam_id = 0
		while True:
			self.cam = cv2.VideoCapture(cam_id)
			if self.cam.grab() is False:
				cam_id += 1
				if cam_id > 3:
					cam_id = 0
			else:
				break
		# I want to see prints everywhere XD	
		self.debug = True
		self.stop = False
		
	@overrides(ReceiverSender)
	def development_function(self):

		if self.stop is True:
			return None

		_, image = self.cam.read()
		try:
			decodedObjects = self.decode(image)
		except Exception as e:
			print('decodeObjetcs error, Error on line {} ... type: {} ... arg e: {}'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))    
		else:	
			for obj in decodedObjects:
				self.queue_send.put({"Type": obj.type, "Data": obj.data})

			if self.debug is True: 
				cv2.imshow("QR_FINDER", image)
				cv2.waitKey(30)

		return True
	
	@overrides(ReceiverSender)
	def execute_message_received(self, message_received):
		print("Code_Reader Received: {}".format(message_received))
		if message_received == "THANK YOU!":
			self.stop = True

