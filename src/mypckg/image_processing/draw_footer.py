'''
Draw a black bottom rectangle with text on it
'''
import cv2

def draw_footer(frame, text,text_font_size_relative=0.5,text_font_size = None):
    '''

    :param frame:
    :param text_font_size: text_font_size = 0.5 * self.video_info['height'] / 480
    :param text:
    :return:
    '''

    t_f_s = text_font_size_relative * frame.shape[0] / 480
    if text_font_size is not None:
        t_f_s = text_font_size

    rect_height = int(40 * t_f_s)
    cv2.rectangle(frame, (0, frame.shape[0] - rect_height),
                  (frame.shape[1], frame.shape[0]), (0, 0, 0),
                  -1)  # draw  backgorund bottom rectangle
    cv2.putText(frame, text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                t_f_s, (255, 255, 255), 2)

    return frame