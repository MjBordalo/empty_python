# import the necessary packages
from datetime import datetime
import time as tm


# TODO:
# class FPM:
# 	def __init__(self):
# 		# store the start time, end time, and total number of frames
# 		# that were examined between the start and end intervals
# 		self._start = None
# 		self._end = None
# 		self._numFrames = 0
#         self.last_computation_datetime = datetime.now()
#
#     def compute_fpm(self):
#         '''
#         Computes number of processed frames per minute. Should be called every time in the main loop
#         :return:
#         '''
#
#         self._numFrames +=1
#         if (datetime.now() - self.last_computation_datetime).seconds >= 15 :
#             self.fpm = self._numFrames*4
#             self.last_computation_datetime = datetime.now()
#             self._numFrames=0
#
#         delta_t = (datetime.now() - self.last_computation_datetime_live ).total_seconds()
#         fps= 1/delta_t
#         self.fpm_live= int(60*fps)
#
#         self.last_computation_datetime_live = datetime.now()


class FPS:
    def __init__(self, numframestoupdateaveragecounting=50):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFramesAverage = 0
        self._numFramesTotal = 0
        self._numFramesInstantaneous = 0


        self.fps_instanatenous = 0
        self.fps_average = 0

        self.last_computation_datetime_instantaneous = None
        self.last_computation_datetime_average = None
        self.numframestoupdateaveragecounting = numframestoupdateaveragecounting


    def start(self):
        # start the timer
        self._start = tm.time()

        self.last_computation_datetime_instantaneous = tm.time()
        self.last_computation_datetime_average = tm.time()

        return self


    def stop(self):
        # stop the timer
        self._end = tm.time()


    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFramesTotal += 1
        self._numFramesAverage += 1
        self._numFramesInstantaneous += 1
        self.last_computation_datetime_instantaneous = tm.time()

        # compute fps instataneous
        self.fps_instanatenous = self._numFramesInstantaneous / (tm.time() - self.last_computation_datetime_instantaneous)

        # compute fps fps_average
        if self._numFramesAverage >= self.numframestoupdateaveragecounting:
            self.fps_average = self._numFramesAverage / (tm.time() - self.last_computation_datetime_average)

            self.last_computation_datetime_average = tm.time()
            self._numFramesAverage = 0


    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        # return (self._end - self._start).total_seconds()
        return (self._end - self._start)


    def get_fps_average(self):
        return self.fps_average


    def get_fps_instanatenous(self):
        return self.fps_instanatenous

    def get_fps_total(self):
        # compute the (approximate) frames per second
        return self._numFramesTotal / self.elapsed()
