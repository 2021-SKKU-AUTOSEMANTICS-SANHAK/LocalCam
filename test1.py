import cv2

video_file = "me.mp4" # 동영상 파일 경로

cap = cv2.VideoCapture(0) # 동영상 캡쳐 객체 생성  ---①
n = 0
if cap.isOpened():                 # 캡쳐 객체 초기화 확인
    while cap.isOpened():
        if cv2.waitKey(1) == ord('q'):  # q to quit
            cv2.destroyAllWindows()
            raise StopIteration
        n += 1
        # _, self.imgs[index] = cap.read()
        cap.grab()
        if n == 10:  # read every 4th frame
            success, im = cap.retrieve()
            print(im.shape)
            if success:
                # img = cv2.resize(im, dsize=(640, 480))
                success, imgenc = cv2.imencode(".jpeg", im)
                n = 0
                cv2.imshow("img", im)
                print(len(imgenc.dumps()))
            else:
                break
        cv2.waitKey(25)  # wait time
else:
    print("can't open video.")      # 캡쳐 객체 초기화 실패
cap.release()                       # 캡쳐 자원 반납
cv2.destroyAllWindows()