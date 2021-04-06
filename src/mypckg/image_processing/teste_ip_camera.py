import cv2
import datetime

# cap = cv2.VideoCapture("rtsp://192.168.1.163:554")
# cap = cv2.VideoCapture('http://192.168.1.163:80')
# cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.163/554")
cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.163:554/11")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps) )
print("Resolution: "+str(width)+"x"+str(width))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (width,height))

start = datetime.datetime.now()
while True:
    ret, frame_orig = cap.read()

    if ret:
        # cv2.imshow('frame_orig', frame_orig)
        out.write(frame_orig)


    key = cv2.waitKey(30) & 0xff
    if key == ord("q"):
        break

    if datetime.timedelta(seconds=20) <= datetime.datetime.now() - start:
        break


cap.release()
out.release()
cv2.destroyAllWindows()

