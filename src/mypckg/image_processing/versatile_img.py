def scale_up(frame,scale_up):
    '''
    Scale the image scale_up% without moving the center
    :param frame:
    :param scale_up: scale percentage [0-100]
    :return:
    '''

    scale_up = 1+ scale_up/100
    s = frame.shape
    # Scale the image 4% without moving the center
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, scale_up)
    frame = cv2.warpAffine(frame, T, (s[1], s[0]))
    return frame
