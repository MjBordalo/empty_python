
import logging
import base64
import cv2


def prepare_picture_telegram(image):
    '''

    :param image: numpy image
    :return: image in string so that mqtt can send it
    '''
    b64str = False
    # look for the right photo
    try:

        is_success, im_buf_arr = cv2.imencode(".jpg", image)
        b64str = im_buf_arr.tobytes()
        b64str = base64.encodebytes(b64str).decode('ascii')

        # enconded_img = image.copy()
        # v = None
        # # method1
        # with io.BytesIO() as f:
        #     imageio.imwrite(f, np.asanyarray(enconded_img, dtype=np.uint8), format='JPEG-FI')
        #
        #     v = f.getvalue()
        #     b64str = base64.standard_b64encode(v)
        #
        #     # f = io.BytesIO()
        #     # w = imageio.get_writer(f, 'jpg')
        #     # w.append_data(np.asanyarray(roi_colored, dtype=np.float64), {'date':'2018-01-01 12:00:00'})
        #     # b64str=f
        #     # with io.BytesIO(result.stdout) as f:
        #     #     bb = f.read()
        #     # b64str = base64.standard_b64encode(roi_colored).decode()
        #
        #     # method2
        #     # b64str = base64.b64encode(np.asanyarray(roi_colored, dtype=np.float64))

    except Exception:
        logging.exception("Error getting img to send")

    return b64str
