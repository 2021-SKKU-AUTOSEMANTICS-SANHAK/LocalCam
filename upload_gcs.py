import cv2
import datetime
import time
import os
from google.cloud import bigquery, storage


credential_path = "atsm-202107-50b0c3dc3869.json"
project_id = 'atsm-202107'
bucket_id = 'sanhak_2021'
dataset_id = 'sanhak_2021'
table_id = 'video'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

storage_client = storage.Client()
client = bigquery.Client()
bucket = storage_client.bucket(bucket_id)


cap = cv2.VideoCapture(0) # 동영상 캡쳐 객체 생성  ---①
cap1 = cv2.VideoCapture('http://192.168.35.226:4747/video')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
n = 0
i = 0
if cap.isOpened() and cap1.isOpened():                 # 캡쳐 객체 초기화 확인
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps1 = cap.get(cv2.CAP_PROP_FPS)
    while i < 2:
        now = time.localtime()
        date_time = time.strftime('%Y-%m-%d_%H-%M-%S', now)
        out = cv2.VideoWriter('./videos/{}'.format(date_time + '_0.avi'), fourcc, fps, (w, h))
        out1 = cv2.VideoWriter('./videos/{}'.format(date_time + '_1.avi'), fourcc, fps1, (w, h))
        if cv2.waitKey(1) == ord('q'):  # q to quit
            cv2.destroyAllWindows()
            raise StopIteration
        start = time.time()
        end = time.time()

        #
        while end - start < 10:
            n += 1
            cap.grab()
            cap1.grab()
            if n == 4:  # read every 6th frame
                success, im = cap.retrieve()
                suc, im1 = cap1.retrieve()
                if success and suc:
                    n = 0
                    cv2.imshow("img", im)
                    cv2.imshow("img1", im1)
                    out.write(im)
                    out1.write(im1)
                else:
                    break
                print(round(end - start))
            cv2.waitKey(25)  # wait time
            end = time.time()

        out.release()
        out1.release()
        print('vid 0,1 uploaded to local directory')
        blob = bucket.blob(date_time + '_0')
        blob1 = bucket.blob(date_time + '_1')
        blob.upload_from_filename('./videos/{}'.format(date_time + '_0.avi'))
        blob1.upload_from_filename('./videos/{}'.format(date_time + '_1.avi'))
        blob.make_public()
        blob1.make_public()
        print('vid 0,1 uploaded to cloud storage')
        vid1_path = 'https://storage.googleapis.com/sanhak_2021/' + date_time + '_0'
        vid2_path = 'https://storage.googleapis.com/sanhak_2021/' + date_time + '_1'
        # query = ("SELECT * FROM {}.{}.{}".format(project_id, dataset_id, table_id))
        query0 = (
            "INSERT INTO {}.{}.{} VALUES('{}', '{}')".format(project_id, dataset_id, table_id + '0', date_time, vid1_path))
        query1 = (
            "INSERT INTO {}.{}.{} VALUES('{}','{}')".format(project_id, dataset_id, table_id + '1', date_time, vid2_path))
        query_job0 = client.query(query0)
        query_job1 = client.query(query1)
        results0 = query_job0.result()
        results1 = query_job1.result()
        print('vid 0,1 paths uploaded to big query')
        i += 1
else:
    print("can't open video.")      # 캡쳐 객체 초기화 실패
cap.release()                       # 캡쳐 자원 반납
cap1.release()
cv2.destroyAllWindows()