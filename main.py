import os
import pickle
from threading import Thread

from google.cloud import firestore
import cv2
import time
import numpy as np



# batch = db.batch()
#
# # Set the data for NYC
# nyc_ref = db.collection(u'video').document(u'NYC')
# batch.set(nyc_ref, {u'name': u'New York City'})
#
# # Commit the batch
# batch.commit()




def update(i, db, cap, fps):
    n = 0
    batch = db.batch()
    while cap.isOpened():
        _, im = cap.read()
        start = time.time()
        end = time.time()

        now = time.localtime()
        col_title = time.strftime('%m%d%H%M%S', now)
        vid_ref = db.collection(u'video{}'.format(i)).document(u'{}'.format(col_title))
        idx = 0
        while end - start < 3:
            n += 1
            cap.grab()
            if n == 8:  # read every 4th frame
                success, im = cap.retrieve()
                cv2.imshow(str(i), im)
                # batch.set(vid_ref, {u'{}'.format(idx): u'{}'.format(im.dumps())})
                batch.set(vid_ref, {u'{}'.format(idx): u'{}'.format(im.tobytes())})
                n = 0
                idx += 1
            # time.sleep(1 / fps)  # wait time
            end = time.time()
        batch.commit()

if __name__ == "__main__":
    credential_path = "C:\LocalCam\mythic-fire-318606-5b15a08cba70.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    db = firestore.Client()

    # cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # fps1 = cap1.get(cv2.CAP_PROP_FPS) % 100
    # fps2 = cap2.get(cv2.CAP_PROP_FPS) % 100
    #
    # thread1 = Thread(target=update, args=([0, db, cap1, fps1]), daemon=True)
    # thread2 = Thread(target=update, args=([1, db, cap2, fps2]), daemon=True)
    #
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()

    im = cv2.imread('keyboard.jpg')
    print(im.tobytes())
    nyc_ref = db.collection(u'video').document(u'NYC')
    nyc_ref.set({u'{keyboard}': u'{}'.format(im.tobytes())})
