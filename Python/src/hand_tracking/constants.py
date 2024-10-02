import mediapipe as mp

# Define finger indices for convenience
FINGER_TIPS = {
    'thumb': mp.solutions.hands.HandLandmark.THUMB_TIP,
    'index': mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP,
    'middle': mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP,
    'ring': mp.solutions.hands.HandLandmark.RING_FINGER_TIP,
    'pinky': mp.solutions.hands.HandLandmark.PINKY_TIP
}

FINGER_PIPS = {
    'thumb': mp.solutions.hands.HandLandmark.THUMB_IP,
    'index': mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP,
    'middle': mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP,
    'ring': mp.solutions.hands.HandLandmark.RING_FINGER_PIP,
    'pinky': mp.solutions.hands.HandLandmark.PINKY_PIP
}

FINGER_DIPs = {
    'thumb': mp.solutions.hands.HandLandmark.THUMB_IP,  # Thumb doesn't have a DIP joint, use IP instead
    'index': mp.solutions.hands.HandLandmark.INDEX_FINGER_DIP,
    'middle': mp.solutions.hands.HandLandmark.MIDDLE_FINGER_DIP,
    'ring': mp.solutions.hands.HandLandmark.RING_FINGER_DIP,
    'pinky': mp.solutions.hands.HandLandmark.PINKY_DIP
}

FINGER_MCPs = {
    'thumb': mp.solutions.hands.HandLandmark.THUMB_MCP,
    'index': mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP,
    'middle': mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP,
    'ring': mp.solutions.hands.HandLandmark.RING_FINGER_MCP,
    'pinky': mp.solutions.hands.HandLandmark.PINKY_MCP
}
