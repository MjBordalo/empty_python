# import the necessary packages
from threading import Thread
import sys
import cv2

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
	from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue

class FileVideoStream_threaded:
	def __init__(self, path, queueSize=128, rotation=0):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		self.stopped = False
		self.rotation = rotation

		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queueSize)

	def start(self):
		# start a thread to read frames from the file video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				return

			# otherwise, ensure the queue has room in it
			if not self.Q.full():
				# read the next frame from the file
				(grabbed, frame) = self.stream.read()

				# if the `grabbed` boolean is `False`, then we have
				# reached the end of the video file
				if not grabbed:
					self.stop()
					return

				# add the frame to the queue
				self.Q.put(frame)

	def read(self):
		# return next frame in the queue
		return self.Q.get()

	def more(self):
		# return True if there are still frames in the queue
		return self.Q.qsize() > 0

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True

	def get_cur_po(self):
		return self.stream.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # Current position of the video file in seconds

	def get_cur_frame(self):
		return self.stream.get(cv2.CAP_PROP_POS_FRAMES)

	def set_cur_frame(self, frame_to_go):
		return self.stream.set(cv2.CAP_PROP_POS_FRAMES, cv2.CAP_PROP_POS_FRAMES+ frame_to_go) # jump to frame

	def get_fps(self):
		return self.stream.get(cv2.CAP_PROP_FPS)

	def get_width(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))

	def get_height(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

	def get_fourcc(self):
		return self.stream.get(cv2.CAP_PROP_FPS)

	def get_num_of_frames(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))

class FileVideoStream:
	def __init__(self, path, rotation=0):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		self.stopped = False
		self.rotation=rotation


	def start(self):
		return self


	def read(self):
		ret, frame = self.stream.read()
		# frame = cv2.flip(frame, 2)

		return True,frame


	def stop(self):
		self.stopped = True
		self.stream.release()

	def get_cur_po(self):
		return self.stream.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # Current position of the video file in seconds

	def get_cur_frame(self):
		return self.stream.get(cv2.CAP_PROP_POS_FRAMES)

	def set_cur_frame(self, frame_to_go):
		return self.stream.set(cv2.CAP_PROP_POS_FRAMES, int(cv2.CAP_PROP_POS_FRAMES+ frame_to_go)) # jump to frame

	def get_fps(self):
		return self.stream.get(cv2.CAP_PROP_FPS)

	def get_width(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))

	def get_height(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

	def get_fourcc(self):
		return self.stream.get(cv2.CAP_PROP_FPS)

	def get_num_of_frames(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))