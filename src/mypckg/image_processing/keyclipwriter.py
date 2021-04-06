# This package allows to record clips using threads and save same frames before and after the event
#from pyimage search: https://www.pyimagesearch.com/2016/02/29/saving-key-event-video-clips-with-opencv/
'''
kcw = KeyClipWriter(bufSize=args["buffer_size"])


While True:
	get frame

	# update the key frame clip buffer
	kcw.update(frame)

	Event happens:
				# if we are not already recording, start recording
			if not kcw.recording:
				timestamp = datetime.datetime.now()
				p = "{}/{}.avi".format(args["output"],
					timestamp.strftime("%Y%m%d-%H%M%S"))
				kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),
					args["fps"])


	# if we are recording and reached a threshold on consecutive
	# number of frames with no action, stop recording the clip
	if kcw.recording and consecFrames == args["buffer_size"]:
		kcw.finish()

# if we are in the middle of recording a clip and movie is finished, wrap it up
if kcw.recording:
	kcw.finish()

'''

from ..python_aux_functions.python_version import VERSION

from collections import deque
from threading import Thread
from queue import Queue
import time
import cv2
from datetime import datetime, timedelta

class KeyClipWriter:
	def __init__(self, bufSize=64, timeout=1.0):
		# store the maximum buffer size of frames to be kept
		# in memory along with the sleep timeout during threading
		self.bufSize = bufSize
		self.timeout = timeout

		# initialize the buffer of frames, queue of frames that
		# need to be written to file, video writer, writer thread,
		# and boolean indicating whether recording has started or not
		self.frames = deque(maxlen=bufSize)
		self.Q = None
		self.writer = None
		self.thread = None
		self.recording = False

		self.init_dt = datetime.now()

	def update(self, frame):
		# update the frames buffer
		self.frames.appendleft(frame)

		# if we are recording, update the queue as well
		if self.recording:
			self.Q.put(frame)

	def start(self, outputPath, fourcc, fps):
		# indicate that we are recording, start the video writer,
		# and initialize the queue of frames that need to be written
		# to the video file

		# do not allow to save in the first two seconds before it was created so that the buffer gets full
		if datetime.now() >= self.init_dt +  timedelta(seconds=3):
			self.recording = True
			self.writer = cv2.VideoWriter(outputPath, fourcc, fps,
				(self.frames[0].shape[1], self.frames[0].shape[0]), True)
			self.Q = Queue()

			# loop over the frames in the deque structure and add them
			# to the queue
			for i in range(len(self.frames), 0, -1):
				self.Q.put(self.frames[i - 1])

			# start a thread write frames to the video file
			self.thread = Thread(target=self.write, args=())
			self.thread.daemon = True
			self.thread.start()

	def write(self):
		# keep looping
		while True:
			# if we are done recording, exit the thread
			if not self.recording:
				return

			# check to see if there are entries in the queue
			if not self.Q.empty():
				# grab the next frame in the queue and write it
				# to the video file
				frame = self.Q.get()
				self.writer.write(frame)

			# otherwise, the queue is empty, so sleep for a bit
			# so we don't waste CPU cycles
			else:
				time.sleep(self.timeout)

	def flush(self):
		# empty the queue by flushing all remaining frames to file
		while not self.Q.empty():
			frame = self.Q.get()
			self.writer.write(frame)

	def finish(self):
		# indicate that we are done recording, join the thread,
		# flush all remaining frames in the queue to file, and
		# release the writer pointer
		self.recording = False
		self.thread.join()
		self.flush()
		self.writer.release()