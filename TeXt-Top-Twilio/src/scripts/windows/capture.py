import VideoCapture as VC
from PIL import Image
from PIL import ImageOps
from subprocess import Popen, PIPE
import time, os, sys

img_name = 'TeXtTop_capture.jpg'

def capture_image(toadd=''):
    toadd = sys.argv[1]
    cam = VC.Device() # initialize the webcam
    img = cam.getImage()
    time.sleep(1) # give sometime for the device to come up
    cam.saveSnapshot(img_name)
    del cam # no longer need the cam. uninitialize
    try:
        send_mail = os.path.abspath(os.path.join(os.path.dirname(__file__),'send mail.py'))
        p = Popen(['python', send_mail, toadd, 'Your capture:', img_name])
    except:
        pass
        os.remove(img_name)
        print "Failed to take and send capture."    
    return img


if __name__ == "__main__":
    capture_image()
    time.sleep(20)
    os.remove(img_name)

