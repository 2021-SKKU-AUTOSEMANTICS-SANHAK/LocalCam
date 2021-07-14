import cv2

cap = cv2.VideoCapture('https://storage.googleapis.com/sanhak_2021/2021-07-14_02-33-20_1')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))


while cv2.waitKey(33) < 0:
    ret, frame = cap.read()
    cv2.imshow("VideoFrame", frame)

cap.release()
# out.release()
cv2.destroyAllWindows()