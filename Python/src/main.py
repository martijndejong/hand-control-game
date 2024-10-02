import cv2
from collections import deque
from hand_tracking.hand_tracking_utils import HandTracker
from hand_tracking.gesture_recognition import recognize_gesture
from communication.socket_client import SocketClient
import json


def main():
    # Initialize the HandTracker.
    hand_tracker = HandTracker()

    # Initialize the SocketClient.
    socket_client = SocketClient(host='localhost', port=65432)
    socket_client.connect()

    # Start capturing video input from the webcam.
    cap = cv2.VideoCapture(0)

    gesture_history = deque(maxlen=5)  # Store the last 5 recognized gestures
    current_gesture = ""
    previous_gesture = ""

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty frame from webcam.")
            continue

        # Flip the image horizontally for a mirror-view display.
        image = cv2.flip(image, 1)

        # Process the image and detect hands.
        results = hand_tracker.process_frame(image)

        gesture = ""

        # Draw hand landmarks on the image and recognize gestures.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks.
                hand_tracker.draw_hand_landmarks(image, hand_landmarks)

                # Recognize gesture.
                recognized_gesture = recognize_gesture(hand_landmarks)
                if recognized_gesture:
                    gesture_history.append(recognized_gesture)
                else:
                    gesture_history.append("")

        else:
            gesture_history.append("")

        # Determine the most frequent gesture in the history
        if gesture_history:
            gesture = max(set(gesture_history), key=gesture_history.count)

        # Check for gesture state change
        if gesture != previous_gesture:
            if previous_gesture:
                # Send stop message for the previous gesture
                stop_message = json.dumps({"action": previous_gesture, "state": "stop"})
                socket_client.send_message(stop_message)
                print(f"Sent stop message: {stop_message}")

            if gesture:
                # Send start message for the new gesture
                start_message = json.dumps({"action": gesture, "state": "start"})
                socket_client.send_message(start_message)
                print(f"Sent start message: {start_message}")

            previous_gesture = gesture

        # Optionally, display the gesture on the image.
        if gesture:
            cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the resulting image.
        cv2.imshow('Hand Tracking', image)

        # Break the loop when 'Esc' key is pressed.
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Release resources.
    cap.release()
    cv2.destroyAllWindows()
    hand_tracker.close()
    socket_client.close()


if __name__ == '__main__':
    main()
