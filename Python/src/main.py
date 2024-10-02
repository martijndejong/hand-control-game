import cv2

# Import the HandTracker class and recognize_gesture function from the hand_tracking package.
from hand_tracking.hand_tracking_utils import HandTracker
from hand_tracking.gesture_recognition import recognize_gesture


def main():
    # Initialize the HandTracker.
    hand_tracker = HandTracker()

    # Start capturing video input from the webcam.
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty frame from webcam.")
            continue

        # Flip the image horizontally for a mirror-view display.
        image = cv2.flip(image, 1)

        # Process the image and detect hands.
        results = hand_tracker.process_frame(image)

        # Draw hand landmarks on the image and recognize gestures.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks.
                hand_tracker.draw_hand_landmarks(image, hand_landmarks)

                # Recognize gesture.
                gesture = recognize_gesture(hand_landmarks)
                if gesture:
                    print(f"Gesture recognized: {gesture}")
                    # TODO: Add code to communicate the gesture to UE.

        # Display the resulting image.
        cv2.imshow('Hand Tracking', image)

        # Break the loop when 'Esc' key is pressed.
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Release resources.
    cap.release()
    cv2.destroyAllWindows()
    hand_tracker.close()


if __name__ == '__main__':
    main()
