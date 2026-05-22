"""
Tracker utilities for OpenCV compatibility
Handles different OpenCV versions and tracker locations
"""

import cv2
import sys


def create_tracker(tracker_type="KCF"):
    """
    Create an OpenCV tracker with support for multiple OpenCV versions.
    
    Args:
        tracker_type (str): Type of tracker - "KCF", "CSRT", or "MOSSE"
    
    Returns:
        cv2.Tracker: The tracker object
    
    Raises:
        ValueError: If tracker type is not supported or not available
    """
    
    tracker_type = tracker_type.upper()
    
    # Try different methods to create trackers based on OpenCV version
    
    # Method 1: Try cv2.TrackerXXX_create() (older versions)
    try:
        if tracker_type == "KCF":
            return cv2.TrackerKCF_create()
        elif tracker_type == "CSRT":
            return cv2.TrackerCSRT_create()
        elif tracker_type == "MOSSE":
            return cv2.TrackerMOSSE_create()
    except AttributeError:
        pass
    
    # Method 2: Try cv2.legacy.TrackerXXX_create() (newer versions)
    try:
        legacy = cv2.legacy
        if tracker_type == "KCF":
            return legacy.TrackerKCF_create()
        elif tracker_type == "CSRT":
            return legacy.TrackerCSRT_create()
        elif tracker_type == "MOSSE":
            return legacy.TrackerMOSSE_create()
    except (AttributeError, NameError):
        pass
    
    # Method 3: Try direct class instantiation
    try:
        if tracker_type == "KCF":
            params = cv2.TrackerKCF_Params()
            return cv2.TrackerKCF(params)
        elif tracker_type == "CSRT":
            params = cv2.TrackerCSRT_Params()
            return cv2.TrackerCSRT(params)
        elif tracker_type == "MOSSE":
            return cv2.TrackerMOSSE_create()
    except (AttributeError, NameError):
        pass
    
    # Method 4: Try cv2.TrackerXXX (without _create)
    try:
        if tracker_type == "KCF":
            return cv2.TrackerKCF()
        elif tracker_type == "CSRT":
            return cv2.TrackerCSRT()
        elif tracker_type == "MOSSE":
            return cv2.TrackerMOSSE()
    except (AttributeError, TypeError):
        pass
    
    # If all methods fail, raise an error
    raise ValueError(
        f"Tracker '{tracker_type}' not available in this OpenCV version.\n"
        f"OpenCV version: {cv2.__version__}\n"
        f"Make sure you installed opencv-contrib-python: pip install --upgrade opencv-contrib-python"
    )


def get_available_trackers():
    """
    Get list of available trackers in current OpenCV version.
    
    Returns:
        list: List of available tracker names
    """
    
    available = []
    
    for tracker_name in ["KCF", "CSRT", "MOSSE"]:
        try:
            create_tracker(tracker_name)
            available.append(tracker_name)
        except ValueError:
            pass
    
    return available


def print_opencv_info():
    """Print OpenCV version and available trackers."""
    print(f"OpenCV version: {cv2.__version__}")
    print(f"OpenCV path: {cv2.__file__}")
    available = get_available_trackers()
    print(f"Available trackers: {', '.join(available) if available else 'None'}")
    
    if not available:
        print("\n⚠️  WARNING: No trackers available!")
        print("Make sure you installed opencv-contrib-python:")
        print("  pip install --upgrade opencv-contrib-python")


if __name__ == "__main__":
    print_opencv_info()
