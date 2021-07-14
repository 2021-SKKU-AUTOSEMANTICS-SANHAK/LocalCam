import cv2
import datetime
import time
import os
from google.cloud import bigquery, storage
import pickle
import numpy as np

credential_path = "C:/LocalCam/atsm-202107-50b0c3dc3869.json"
project_id = 'atsm-202107'
dataset_id = 'sanhak_2021'
table_id = 'video0'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


client = bigquery.Client()
# storage_client = storage.Client()

im = cv2.imread('keyboard.jpg')
dst = cv2.resize(im, dsize=(640, 480))

success, tmp = cv2.imencode(".jpeg", dst)

ret = tmp.dumps()


# now = time.localtime()
# date_time = time.strftime('%Y-%m-%d %H:%M:%S', now)
# b = b'Vi er s\xc3\xa5 glad for \xc3\xa5 h\xc3\xb8re og l\xc3\xa6re'
#
# # query = ("INSERT INTO {}.{}.{} VALUES({}, CAST({} AS BYTES))".format(project_id, dataset_id, table_id, '\''+date_time+'\'', ret))
# query = (
#             "INSERT INTO {}.{}.{} VALUES('{}', '{}', '{}')".format(project_id, dataset_id, table_id, '2020-01-01_01-02-01', 'abc',
#                                                              'abcd'))
# query = ("SELECT vid FROM {}.{}.{} WHERE time='2021-07-09T16:28:04' LIMIT 1".format(project_id, dataset_id, table_id))
query = ("SELECT datetime, path FROM {}.{}.{} ORDER BY datetime LIMIT 1".format(project_id, dataset_id, table_id))
# query = ("DELETE FROM {}.{}.{} WHERE datetime = '2021-07-12_10-38-48'".format(project_id, dataset_id, table_id))
query_job = client.query(query)
results = query_job.result()


# print(ret)
# abc = pickle.loads(ret)
# print(cv2.imdecode(abc, cv2.IMREAD_COLOR))

# is_exist = len(list(results))
# print(is_exist)
#
for row in results:
    ret = row.path
    print(ret)