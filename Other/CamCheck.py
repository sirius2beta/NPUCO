import cv2
import sys

def list_cameras(max_tested = 10):
    index = 0
    arr = []
    while index < max_tested:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
    return arr

def open_cameras(camera_indexes):
    caps = [cv2.VideoCapture(i) for i in camera_indexes]
    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f'Camera {i}', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_indexes = list_cameras()
    if not camera_indexes:
        print("No Camera.")
        sys.exit()

    print(f"Video : {camera_indexes}")
    open_cameras(camera_indexes)

