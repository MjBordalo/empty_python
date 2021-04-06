# recordvideo.py
# this allow to save video from pi or usbwebcam
#
# example : python recordvideo.py  -mode camera -src /dev/cameraA -resolution 1280x960  -delay 1

'''
NOTES:
     to save in real time you probably have to set fps to a value around 5 fps or lower (if no delay is set it will try to do a real time video) if its looking to fast its because you have to lower the fps
     to do a timelapse you just have to set the delay flag (yoy can also ajust the number of fps)
'''
import sys
# sys.path.append('../')
import time
import cv2
# from vs.videostream import VideoStream
from datetime import datetime
import time
import argparse


'''Parser'''
parser = argparse.ArgumentParser(description='Record video')

parser.add_argument('-mode', '-Mode', help='choose the video input source: possible: [camera,pi]',default="camera", choices=['camera', 'pi'])
parser.add_argument('-resolution', '-r', help="define camera resolution.put 'x' in the middle", default=False)
parser.add_argument('-src', '-Src', help='choose the camera source (int)', default=0)
parser.add_argument('-delay', '-d', help='time delay betweeen frames',default=0)
parser.add_argument('-duration', '-du', help='to automatically finish recording',default=0)
parser.add_argument('-fps', help='frames per secound',default=10)


if not parser.parse_args().resolution:
	resolution =(640,480)
else:
	resolution = map(int, parser.parse_args().resolution.split('x'))
	resolution = (resolution[0],resolution[1])

src = parser.parse_args().src
delay = float(parser.parse_args().delay)
mode = parser.parse_args().mode
fps = int(parser.parse_args().fps)
duration = int(parser.parse_args().duration)


usePiCamera=0
if mode == "pi":
	usePiCamera = 1


'''Record video'''
# vs= VideoStream(src=src,usePiCamera=usePiCamera,resolution=resolution )
vs = cv2.VideoCapture(src)
# vs.start()
time.sleep(3)


fourcc = cv2.VideoWriter_fourcc(*'XVID')
filename = str(mode)+'_'+datetime.now().strftime("%Y_%m_%d-%H_%M")+'.avi'
if mode == "camera":
	# filename = src.split("/")[-1] + '_' + str(datetime.now().date()) + '.avi'
	filename = "camera"+ '_'+ datetime.now().strftime("%Y_%m_%d-%H_%M") + '.avi'

if delay == 0:
	delay=1./fps


print("Going to capture:")
print("    filename: " +str(filename))
print("    fourcc: "+ str(fourcc))
print("    resolution: "+str(resolution))
print("    delay (seconds): "+str(delay))
print("    duration (seconds): "+str(duration))
print("    fps: "+str(fps))

out = cv2.VideoWriter(filename, fourcc, fps, resolution )

print ("Press 'q' key on image to finish recording")

begin = int(datetime.now().strftime("%s"))

while True:
	gotit, image = vs.read()

	if gotit :
		print("frame plote "+ str(datetime.now().time()) )
		out.write(image)

		# show the frame
		cv2.imshow("Frame", cv2.resize(image,resolution))
		key = cv2.waitKey(1) & 0xFF

		time.sleep(delay)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
	if duration != 0 and int(datetime.now().strftime("%s")) - begin > duration:
		print("Automatically breaking cause its time for that!")
		break




print("Finish recording: "+str(filename))
# vs.stop()
out.release()
cv2.destroyAllWindows()

# # import the necessary packages
# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time
# import cv2
#
#
# #blabla22323423wewrwr1231231231weqweqweqw
#
# # initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 1
# # camera.hflip = True
# # camera.vflip = True
# rawCapture = PiRGBArray(camera, size=(640, 480))
#
# # allow the camera to warmup
# time.sleep(2)
#
#
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 32, (640,480))
#
# # capture frames from the camera
# last_time=0
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
# 	# grab the raw NumPy array representing the image, then initialize the timestamp
# 	# and occupied/unoccupied text
# 	image = frame.array
# 	now_time =int(time.time())
# 	# if (now_time % 1==0 & last_time != now_time ):
# 	# 	last_time = now_time
# 	time.sleep(10)
# 	print "frame plote "+ str(now_time)
# 	out.write(image)
#
# 	# show the frame
# 	cv2.imshow("Frame", image)
# 	key = cv2.waitKey(1) & 0xFF
#
# 	# clear the stream in preparation for the next frame
# 	rawCapture.truncate(0)
#
# 	# if the `q` key was pressed, break from the loop
# 	if key == ord("q"):
# 		break
#
#
# out.release()
#
# cv2.destroyAllWindows()
