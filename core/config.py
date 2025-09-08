from cvzone.ColorModule import ColorFinder

# Creates an object for color detection (debug mode: False)
myColorFinder = ColorFinder(False)

# Frame intervals in seconds for different frame rates
FRAMES_IN_SECOND = {
    "FPS_30": 0.033978933061,    # ~1/29.42
    "FPS_60": 0.0169262017603,   # ~1/59.08
    "FPS_120": 0.0084796095462,  # ~1/117.9
    "FPS_240": 0.0043110881,     # ~1/232
}

# Minimum area of a detected object (in pixels) to be considered found
MIN_AREA = 5000
