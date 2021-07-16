import cv2
import time
from google.cloud import bigquery, storage


def receive_send(args):
    sources = args['sources']
    frame_skip = args['frame_skip']
    video_len = args['video_length']
    how_many = args['how_many']
    project_id = args['project_id']
    bucket_id = args['bucket_id']
    dataset_id = args['dataset_id']
    table_id = 'video_sec-{}_frame-{}'.format(str(video_len), str(frame_skip))
    gcs_dir = list()
    cap = list()
    fps = list()
    out = list()
    blob = list()
    cam_num = len(sources)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    w = 640
    h = 480

    storage_client = storage.Client()
    client = bigquery.Client()
    bucket = storage_client.bucket(bucket_id)

    for i in range(cam_num):
        gcs_dir.append('cam-{}_sec-{}_frame-{}'.format(i, video_len, frame_skip))
        cap.append(cv2.VideoCapture(sources[i]))
        cap[i].set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap[i].set(cv2.CAP_PROP_FRAME_HEIGHT, h)

        if not cap[i].isOpened():
            print('cam #{} is not open'.format(i))
            return None

        fps.append(cap[i].get(cv2.CAP_PROP_FPS))

    if how_many == 'realtime':
        realtime = True
    else:
        realtime = False

    iter_num = 0
    frame_skip_idx = 0
    while True:
        if not realtime and iter_num >= how_many:
            break

        if cv2.waitKey(1) == ord('q'):  # q to quit
            cv2.destroyAllWindows()
            raise StopIteration

        now = time.localtime()
        date_time = time.strftime('%Y-%m-%d_%H-%M-%S', now)
        for i in range(cam_num):
            out.append(cv2.VideoWriter(
                './videos/{}'.format(date_time + '_{}.avi'.format(i)), fourcc, fps[i], (w, h)))

        start = time.time()
        end = time.time()

        while end - start < video_len:
            frame_skip_idx += 1
            for i in cap:
                i.grab()
            if frame_skip_idx == frame_skip:
                for i, cp in enumerate(cap):
                    success, im = cp.retrieve()
                    if success:
                        frame_skip_idx = 0
                        cv2.imshow(str(i), im)
                        out[i].write(im)
                    else:
                        break   # 한번에 처리안해서 data 꼬일 수 있음
                print(round(end - start))
            cv2.waitKey(25)  # wait time
            end = time.time()

        for i in range(cam_num):
            out[i].release()
            blob = bucket.blob(gcs_dir[i] + '/' + date_time + '_' + str(i))
            blob.upload_from_filename('./videos/{}'.format(date_time + '_{}.avi'.format(i)))
            blob.make_public()
            vid_path = 'https://storage.googleapis.com/{}/{}/'.format(bucket_id, gcs_dir[i]) + date_time + '_0'
            query = (
                "INSERT INTO `{}.{}.{}` VALUES({}, '{}', '{}')".format(project_id, dataset_id, table_id, str(i), date_time,
                                                                       vid_path))
            query_job = client.query(query)
            results = query_job.result()
        iter_num += 1
        print(str(iter_num) + 'nd upload succeed')

    for i in cap:
        i.release()
    cv2.destroyAllWindows()
