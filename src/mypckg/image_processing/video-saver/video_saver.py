import time 
import cv2

from datetime import datetime, timedelta
from threading import Thread

from python_file_manager.file_manager import Manager 


class video_saver(Thread):

    def __init__(self, open_id, save_folder_path, fourcc=None, duration=120):
        Thread.__init__(self)
        self.id_cam = open_id
        self.folder_path = save_folder_path
        if fourcc is None:
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        else:
            self.fourcc = fourcc    

        self.f_h = Manager("error")
        self.f_h.create_folder(save_folder_path)
        self.f_h.create_logger()

        self.info_h = Manager("info")

        self.info_h.create_logger()
        self.logger = self.info_h.logger

        self.duration = duration

    def record_video(self, video_folder):
        try:
            self.logger.info("Initialized at: {}".format(video_folder))
            cap = cv2.VideoCapture(self.id_cam, cv2.CAP_DSHOW)

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            


            start = datetime.now() 
            
            video_name = video_folder + "/" + "{}_{}_{}.avi".format(start.hour, start.minute, start.second)
            print(video_name)
            out = cv2.VideoWriter(video_name, self.fourcc, fps, (width, height))
        except Exception as e:
            self.f_h.error_message(" wrong capture ", e)
            return 
        else:    
            while True: 
                ret, frame_orig = cap.read()

                if ret:
                    out.write(frame_orig)

                key = cv2.waitKey(30) & 0xff
                if key == ord("q"):
                    break

                if timedelta(seconds=self.duration) <= datetime.now() - start:
                    self.logger.info("Video finished at: {}".format(video_name))
                    break

    def create_today_dir(self):
        now = datetime.now()
        now_date = now.date()
        folder_path = self.folder_path + "/" + "{}".format(now_date)
        self.f_h.create_folder( folder_path )
        return folder_path

    def run(self):
        while True:
            folder_path = self.create_today_dir()
            self.record_video(folder_path)

def cam_init(cam_id, folder_path):

    ip_saver = video_saver(cam_id, folder_path)
    ip_saver.daemon = True
    ip_saver.start()



if __name__ == "__main__":
    ip_cam = "rtsp://admin:123456@192.168.1.110:554/live/ch0"
    entry_cam = 2
    non_entry_cam = 0

    cam_init(ip_cam, "/home/ts-aves/videos/ip_cam")
    cam_init(non_entry_cam, "/home/ts-aves/videos/non_entry_cam")
    cam_init(entry_cam, "/home/ts-aves/videos/entry_cam")

    while True:
        pass
