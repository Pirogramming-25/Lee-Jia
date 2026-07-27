import cv2 as cv
import mediapipe as mp
import math
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from visualization import draw_manual, print_RSP_result

def calc_distance(p1, p2):
    """두 랜드마크 사이의 3D 거리 계산.
    랜드마크는 .x, .y, .z 를 가진 객체입니다 (0~1 사이 정규화 좌표)."""
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2 +
        (p1.z - p2.z) ** 2
    )


def is_finger_open(landmarks, tip_idx, pip_idx, wrist_idx=0):
    """TIP과 손목의 거리 > PIP과 손목의 거리 이면 손가락이 펴진 것.
    (자료에서 알려준 판별 규칙 그대로)"""
    tip_dist = calc_distance(landmarks[tip_idx], landmarks[wrist_idx])
    pip_dist = calc_distance(landmarks[pip_idx], landmarks[wrist_idx])
    return tip_dist > pip_dist


def classify_rps(landmarks):
    """펴진 손가락 개수로 가위/바위/보 판별.
    반환값 규약은 스켈레톤 print_RSP_result 와 동일:
       0 = Rock, 1 = Paper, 2 = Scissors, None = 판별 실패
    """

    finger_pairs = [
        (8, 6),
        (12, 10),
        (16, 14),
        (20, 18),
    ]

    open_count = sum(
        1 for tip, pip in finger_pairs
        if is_finger_open(landmarks, tip, pip)
    )

    if open_count == 0:
        return 0
    elif open_count == 2:
        return 2
    elif open_count >= 4:
        return 1
    else:
        return None


latest_result = None


def result_callback(result: vision.HandLandmarkerResult,
                    output_image: mp.Image,
                    timestamp_ms: int):
    global latest_result
    latest_result = result

def main():
    global latest_result


    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=result_callback,
    )


    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    start_time = time.time()


    with vision.HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame. Exiting ...")
                break

            frame = cv.flip(frame, 1)

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            timestamp_ms = int((time.time() - start_time) * 1000)
            landmarker.detect_async(mp_image, timestamp_ms)

            rps_result = None
            if latest_result is not None and latest_result.hand_landmarks:
  
                frame = draw_manual(frame, latest_result)
                hand_landmarks = latest_result.hand_landmarks[0]
                rps_result = classify_rps(hand_landmarks)

            frame = print_RSP_result(frame, rps_result)

            cv.imshow('Rock Paper Scissors', frame)


            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()