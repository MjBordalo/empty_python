# import the necessary packages
# from imutils.video import *
from .webcamvideostream import WebcamVideoStream
from .filevideostream import FileVideoStream

class VideoStream(object):
	def __init__(self, src=0, usePiCamera=False, useFileVideo=False, resolution=(320, 240),framerate=32, fourcc=None):
		# check to see if the picamera module should be used
		if usePiCamera:
			# only import the picamera packages unless we are
			# explicity told to do so -- this helps remove the
			# requirement of `picamera[array]` from desktops or
			# laptops that still want to use the `imutils` package
			from .pivideostream import PiVideoStream

			# initialize the picamera stream and allow the camera
			# sensor to warmup
			self.stream = PiVideoStream(resolution=resolution, framerate=framerate)

		elif useFileVideo:
			self.stream = FileVideoStream(src)

		# otherwise, we are using OpenCV so initialize the webcam
		# stream
		else:
			self.stream = WebcamVideoStream(src=src,resolution=resolution, fps=framerate,fourcc = fourcc)


	def start(self):
		# start the threaded video stream
		x = self.stream.start()

		self.fps = self.stream.get_fps()
		self.width = self.stream.get_width()
		self.height = self.stream.get_height()
		self.fourcc = self.get_fourcc()
		self.num_of_frames = self.stream.get_num_of_frames()

		return x

	def restart(self):
		return self.stream.restart()

	def update(self):
		# grab the next frame from the stream
		self.stream.update()

	def read(self):
		# return the current frame
		return self.stream.read()

	def stop(self):
		# stop the thread and release any resources
		self.stream.stop()

	def set_cur_frame(self, frame_to_go):
		self.stream.set_cur_frame(frame_to_go)

	def get_cur_po(self):
		return self.stream.get_cur_po()

	def get_cur_frame(self):
		return self.stream.get_cur_frame()

	def get_fps(self):
		return self.stream.get_fps()

	def get_width(self):
		return self.stream.get_width()

	def get_height(self):
		return self.stream.get_height()

	def get_fourcc(self):
		return self.stream.get_fourcc()

	def get_num_of_frames(self):
		return self.stream.get_num_of_frames()

	def is_open(self):
		return self.stream.is_open()

	def grab(self):
		self.stream.grab()

