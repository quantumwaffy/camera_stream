import consts
import cv2
import data_structures as structs
import mediapipe as mp
import numpy

handsModule = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils


class Detector:
    def __init__(
        self,
        camera_uri: str = "/dev/video0",
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        frame_width: int = 1920,
        frame_height: int = 1080,
        alfa: float = 0.3,
        activation_style_config: structs.Style = structs.Style(0, 255, 0, cv2.FILLED),  # noqa
        correction_style_config: structs.Style = structs.Style(255, 255, 0, cv2.FILLED),  # noqa
        confirmation_style_config: structs.Style = structs.Style(255, 0, 0, cv2.FILLED),  # noqa
    ) -> None:
        self._video_capture: cv2.VideoCapture = cv2.VideoCapture(camera_uri)
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self._mp_hands: handsModule.Hands = handsModule.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._launched: bool = False
        self._frame_width: int = frame_width
        self._frame_height: int = frame_height
        self._alfa: float = alfa
        self._activation_zone: structs.Rectangle = self._get_zone(activation_style_config, 3)
        self._correction_zone: structs.Rectangle = self._get_zone(correction_style_config, 2)
        self._confirmation_zone: structs.Rectangle = self._get_zone(confirmation_style_config, 1)
        self._current_zone: consts.ZoneTopicType | None = None

    def _get_zone(self, style: structs.Style, multiplier: int) -> structs.Rectangle:
        sector_y: int = self._frame_height // 3
        end_y: int = sector_y * multiplier
        start_y: int = end_y - sector_y
        return structs.Rectangle(structs.Point(0, start_y), structs.Point(self._frame_width, end_y), style)

    def _get_frame(self) -> numpy.ndarray:
        _, image = self._video_capture.read()
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def _get_processed_image(self, img: numpy.ndarray) -> numpy.ndarray:
        overlay: numpy.ndarray = img.copy()
        self._draw_separators(overlay)
        return cv2.addWeighted(overlay, self._alfa, img, 1 - self._alfa, 0)

    def _draw_separators(self, img: numpy.ndarray) -> None:
        for zone in (self._activation_zone, self._correction_zone, self._confirmation_zone):
            cv2.rectangle(img, zone.start.coords, zone.end.coords, zone.style.bgr, zone.style.thickness)

    @staticmethod
    def _draw_hands(img: numpy.ndarray, landmarks) -> None:
        for hand_landmarks in landmarks:
            for land_mark in hand_landmarks.landmark:
                h, w, c = img.shape
                cx, cy = int(land_mark.x), int(land_mark.y * h)
                cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, hand_landmarks, handsModule.HAND_CONNECTIONS)

    def _send_msg(self, detected_zone: consts.ZoneTopicType) -> None:
        if self._current_zone is detected_zone:
            return None
        self._current_zone = detected_zone
        print(self._current_zone.value)

    def run(self) -> None:
        while True:
            img: numpy.ndarray = self._get_processed_image(self._get_frame())
            results = self._mp_hands.process(img)
            if landmarks := results.multi_hand_landmarks:
                if len(results.multi_handedness) == 1:
                    index_tip = landmarks[0].landmark[handsModule.HandLandmark.INDEX_FINGER_TIP]
                    index_tip_y: float = index_tip.y * 1000
                    if self._activation_zone.start.y <= index_tip_y <= self._activation_zone.end.y:
                        self._send_msg(consts.ZoneTopicType.ACTIVATION)
                    elif self._correction_zone.start.y <= index_tip_y <= self._correction_zone.end.y:
                        self._send_msg(consts.ZoneTopicType.CORRECTION)
                    elif self._confirmation_zone.start.y <= index_tip_y <= self._confirmation_zone.end.y:
                        self._send_msg(consts.ZoneTopicType.CONFIRMATION)
                    else:
                        print("Not found")
                self._draw_hands(img, landmarks)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    Detector().run()
