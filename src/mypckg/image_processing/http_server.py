#!/usr/bin/python
'''
	Author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server


	use python 2

	dependencies:
'''
# import cv2
import numpy as np
from PIL import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
capture=None


SERVER_IP = 'localhost'
SERVER_IP = '10.8.0.114'
SERVER_IP = '92.222.68.85'
class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.endswith('cam2.mjpg'):
			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			while True:
				try:
					#red from webcam
					# rc,img = capture.read()
					# if not rc:
					# 	continue

					filename = '/home/mjbordalo/example.jpg'
					#Read from file using cv2
					# img = cv2.imread(filename)
					# imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

					#Read from file using PIL
					img = Image.open(filename)
					img = np.array(img)
					imgRGB = img


					jpg = Image.fromarray(imgRGB)
					tmpFile = StringIO.StringIO()
					jpg.save(tmpFile,'JPEG')
					self.wfile.write("--jpgboundary")
					self.send_header('Content-type','image/jpeg')
					self.send_header('Content-length',str(tmpFile.len))
					self.end_headers()
					jpg.save(self.wfile,'JPEG')
					time.sleep(0.05)
				except KeyboardInterrupt:
					break
			return

		if self.path.endswith('cam1.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<img src="http://127.0.0.1:8080/cam1.mjpg"/>')
			self.wfile.write('</body></html>')
			print("I was here")
			return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def main():
	global capture
	#capture = cv2.VideoCapture(0)
	# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
	# capture.set(cv2.CAP_PROP_SATURATION,0.2)
	global img
	try:
		server = ThreadedHTTPServer((SERVER_IP, 5555), CamHandler)
		print("server started1")
		server.serve_forever()

	except KeyboardInterrupt:
		#capture.release()
		server.socket.close()

if __name__ == '__main__':
	main()
