# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

from datetime import datetime

class PiVideoStream:

	def __init__(self, resolution=(320, 240), framerate=32, rotation = 0):
		# initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution

		self.camera.framerate = framerate
		self.camera.rotation = rotation
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False

		#edited by me:
		self.cur_frame = 0
		self.init_time = datetime.now()



	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)

			# if the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return

	def read(self):
		# return the frame most recently read

		#edited by me
		self.cur_frame+=1

		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True


	def get_cur_po(self):
		return int((datetime.now()-self.init_time).total_seconds())

	def get_cur_frame(self):
		return self.cur_frame

	def get_fps(self):
		return self.camera.framerate

	def get_width(self):
		return self.camera.resolution[0]

	def get_height(self):
		return self.camera.resolution[1]

	def get_fourcc(self):
		return None

	def get_num_of_frames(self):
		return 0


if __name__ == "__main__":

	print("Press 'q' key to close the window")
	c = PiVideoStream()
	c.start()
	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	while True:
		cv2.imshow('frame',c.read())
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	c.stop()