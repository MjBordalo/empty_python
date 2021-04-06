# import the necessary packages
from threading import Thread
import cv2
from datetime import datetime

class WebcamVideoStream:
	def __init__(self, src=0,resolution=(640,480), fps=5):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = None
		self.src = src
		self.resolution=resolution
		self.fps=fps
		self.stopped = False
		self.cur_frame=0
		self.init_time = datetime.now()
		self.t=None

		self.restart()
		# initialize the variable used to indicate if the thread should
		# be stopped


	def start(self):
		# start the thread to read frames from the video stream
		# self.t = Thread(target=self.update, args=())
		# self.t.daemon = True
		# self.t.start()
		return self

	def restart(self):
		if self.stream:
			self.stop()
		self.stream = cv2.VideoCapture(self.src)
		self.stream.set(3, self.resolution[0])
		self.stream.set(4, self.resolution[1])
		# (self.grabbed, self.frame) = self.stream.read()
		# self.start()

		self.stream.set(cv2.CAP_PROP_FPS, self.fps)

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		self.cur_frame+=1
		(self.grabbed, self.frame) = self.stream.read()
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
		self.stream.release()

	def get_cur_po(self):
		return int((datetime.now()-self.init_time).total_seconds())


	def get_cur_frame(self):
		return self.cur_frame

	# def get_cur_po(self):
	# 	return self.stream.get(cv2.CAP_PROP_POS_MSEC) / 1000.0 # Current position of the video file in seconds
    #
	# def get_cur_frame(self):
	# 	return self.stream.get(cv2.CAP_PROP_POS_FRAMES)


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


if __name__ == "__main__":
	import argparse

	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-src", "-Src", type=int, default=0,
					help="choose the camera src")
	args = vars(ap.parse_args())
	print("Press 'q' key to close the window")
	c = WebcamVideoStream(src=args["src"])
	c.start()
	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	while True:
		cv2.imshow('frame',c.read())
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	c.stop()