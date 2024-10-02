import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # Initialize MediaPipe Hands and Drawing utils.
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

        # Set up the MediaPipe Hands model.
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # For real-time video input.
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )

    def process_frame(self, image):
        """
        Processes an image frame to detect hands.

        Args:
            image: The input BGR image.

        Returns:
            results: The hand detection results.
        """
        # Convert the BGR image to RGB as MediaPipe uses RGB.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the image and detect hands.
        results = self.hands.process(image_rgb)
        return results

    def draw_hand_landmarks(self, image, hand_landmarks):
        """
        Draws hand landmarks and connections on the image.

        Args:
            image: The input BGR image.
            hand_landmarks: The hand landmarks to draw.
        """
        self.mp_drawing.draw_landmarks(
            image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def close(self):
        """Releases the MediaPipe resources."""
        self.hands.close()
