import mediapipe as mp

# Define finger indices for convenience
from .constants import FINGER_TIPS, FINGER_PIPS, FINGER_DIPs, FINGER_MCPs

THUMB_MOVE_THRESHOLD = 0.07


def _is_finger_extended(hand_landmarks, finger_name) -> bool:
    """
    Determines if a finger is extended.
    """
    tip_id = FINGER_TIPS[finger_name]
    pip_id = FINGER_PIPS[finger_name]
    dip_id = FINGER_DIPs[finger_name]
    mcp_id = FINGER_MCPs[finger_name]

    tip = hand_landmarks.landmark[tip_id]
    pip = hand_landmarks.landmark[pip_id]
    dip = hand_landmarks.landmark[dip_id]
    mcp = hand_landmarks.landmark[mcp_id]

    if finger_name == 'thumb':
        # For the thumb, compare x-coordinates relative to the wrist
        wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
        return abs(tip.x - wrist.x) > abs(mcp.x - wrist.x)
    else:
        # Finger is extended if TIP is above PIP and DIP joints
        return tip.y < dip.y < pip.y < mcp.y


def _get_thumb_direction(hand_landmarks) -> str:
    """
    Determines the direction the thumb is pointing.
    Returns 'left', 'right', or None.
    """
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    thumb_mcp = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_CMC]

    # Calculate the vector of the thumb
    thumb_vector_x = thumb_tip.x - thumb_mcp.x

    if thumb_vector_x > THUMB_MOVE_THRESHOLD:
        return 'right'
    elif thumb_vector_x < -THUMB_MOVE_THRESHOLD:
        return 'left'
    else:
        return ""


def recognize_gesture(hand_landmarks) -> str:
    """
    Recognizes gestures based on hand landmarks.

    Args:
        hand_landmarks: The landmarks of the detected hand.

    Returns:
        gesture: A string representing the recognized gesture, or an empty string if no gesture is recognized.
    """
    # Check if fingers are extended
    fingers = {}
    for finger in ['thumb', 'index', 'middle', 'ring', 'pinky']:
        fingers[finger] = _is_finger_extended(hand_landmarks, finger)

    thumb_direction = _get_thumb_direction(hand_landmarks)

    # Gesture 1: Closed Fist with One Finger Pointing Up (Jump)
    if fingers['index'] and not any([fingers['middle'], fingers['ring'], fingers['pinky'], fingers['thumb']]):
        return 'Jump'

    # Gesture 2: Closed Fist with Thumb Pointing Right (Move Right)
    if fingers['thumb'] and thumb_direction == 'right' and not any(
            [fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']]):
        return 'Move Right'

    # Gesture 3: Closed Fist with Thumb Pointing Left (Move Left)
    if fingers['thumb'] and thumb_direction == 'left' and not any(
            [fingers['index'], fingers['middle'], fingers['ring'], fingers['pinky']]):
        return 'Move Left'

    # Gesture 4: Thumb Pointing Right with Index Finger Up (Move Right and Jump)
    if fingers['thumb'] and fingers['index'] and thumb_direction == 'right' and not any(
            [fingers['middle'], fingers['ring'], fingers['pinky']]):
        return 'Move Right and Jump'

    # Gesture 5: Thumb Pointing Left with Index Finger Up (Move Left and Jump)
    if fingers['thumb'] and fingers['index'] and thumb_direction == 'left' and not any(
            [fingers['middle'], fingers['ring'], fingers['pinky']]):
        return 'Move Left and Jump'

    # No recognized gesture
    return ""
