import sys
import time

import cv2

import frcballtracker.aerialassist


def stream_video(path, callback):
    cap = cv2.VideoCapture(path)
    last_frame_time = last_second_time = time.perf_counter()
    frames_passed = 0
    fps = 30
    while cap.isOpened():
        cap.grab()
        _, image = cap.retrieve()

        image = cv2.pyrDown(image)

        result = callback(image)
        if result is not None:
            cv2.imshow("Demo", result)

        time_now = time.perf_counter()
        key = cv2.waitKey(max(1, 33 - int(1000 * time_now - last_frame_time)))
        print(f"FPS: {fps:.2f}")

        last_frame_time = time_now
        frames_passed += 1
        if time_now - last_second_time >= 1:
            last_second_time = time_now
            fps = frames_passed
            frames_passed = 0

        if key == 27:
            break
        elif key == 32:
            cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


def main():
    stream_video(frcballtracker.aerialassist.video, frcballtracker.aerialassist.process_image)
    sys.exit(0)


if __name__ == '__main__':
    main()
