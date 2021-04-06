# import the necessary packages
from threading import Thread
import cv2
from datetime import datetime

class WebcamVideoStream:
	def __init__(self, src=0,resolution=(640,480), fps=5, threaded=False, fourcc = None):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = None
		self.src = src
		self.resolution=resolution
		self.fps=fps
		self.fourcc = fourcc

		self.stopped = True
		self.cur_frame=0
		self.init_time = datetime.now()

		self.threaded = threaded
		if threaded:
			self.grabbed = False
			self.frame = None
			self.t=None

		# self.restart()
		# initialize the variable used to indicate if the thread should
		# be stopped


	def start(self):
		self.stream = cv2.VideoCapture(self.src)
		self.stream.set(3, self.resolution[0])
		self.stream.set(4, self.resolution[1])
		self.stream.set(cv2.CAP_PROP_FPS, self.fps)
		if self.fourcc is not None:
			if self.fourcc == "MJPG":
				fourcc = cv2.VideoWriter_fourcc(*'MJPG')
			elif self.fourcc == "YUYV":
				fourcc = cv2.VideoWriter_fourcc(*'YUYV')
			self.stream.set(cv2.CAP_PROP_FOURCC, fourcc)

		self.stopped = False
		if self.threaded:
			# start the thread to read frames from the video stream
			self.t = Thread(target=self.update, args=())
			self.t.daemon = True
			self.t.start()

		return self

	def restart(self):
		if not self.stopped :
			self.stop()
		self.start()

		# self.stream = cv2.VideoCapture(self.src)
		# self.stream.set(3, self.resolution[0])
		# self.stream.set(4, self.resolution[1])
		# (self.grabbed, self.frame) = self.stream.read()
		# self.start()


	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			# (self.grabbed, self.frame) = self.stream.read()
			self._read()

	def _read(self):
		# return the frame most recently read
		self.cur_frame+=1
		(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		if self.threaded:
			return (self.grabbed, self.frame)
		else:
			self.cur_frame += 1
			return self.stream.read()

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

	def get_format(self):
		return self.stream.get(cv2.CAP_PROP_FORMAT)

	def get_width(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))

	def get_height(self):
		return int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

	def get_fourcc(self):
		return self.stream.get(cv2.CAP_PROP_FPS)

	def get_num_of_frames(self):
		return int(0)

	def is_open(self):
		return self.stream.isOpened()

	def grab(self):
		return self.stream.grab()

if __name__ == "__main__":
	import argparse

	font = cv2.FONT_HERSHEY_SIMPLEX
	topLeftCornerOfText = (10, 20)
	fontScale = 1
	fontColor = (255, 255, 255)
	lineType = 2


	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-src", "-Src", type=int, default=0,
					help="choose the camera src")
	ap.add_argument('-resolution', '-r', help="define camera resolution.put 'x' in the middle", default=False)
	ap.add_argument('-fps', help="define fprames per second", default=3, type=int)
	ap.add_argument('-threaded', help="get rames in separated thread", default=0)

	args = vars(ap.parse_args())

	if not args["resolution"]:
		resolution = (640, 480)
	else:
		resolution = map(int, args["resolution"].split('x'))
		resolution = (resolution[0], resolution[1])

	print("Press 'q' key to close the window")
	c = WebcamVideoStream(src=args["src"], resolution=resolution, fps=int(args["fps"]), threaded=args["threaded"])
	c.start()
	# cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	cv2.namedWindow('frame')

	print("Going to capture:")
	print("    resolution: " + str(c.get_width())+ "x"+ str(c.get_height()))
	print("    fps: " + str(c.get_fps()))
	print("    format: " + str(c.get_format()))
	while True:
		grabbed, frame = c.read()
		if grabbed:
			cv2.putText(frame, str(c.get_cur_frame()),
						topLeftCornerOfText,
						font,
						fontScale,
						fontColor,
						lineType)

			img = cv2.imshow('frame',frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break


	# When everything done, release the capture
	c.stop()