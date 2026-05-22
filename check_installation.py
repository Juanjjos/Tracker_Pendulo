#!/usr/bin/env python3
"""
Quick test to verify the installation is working correctly
Run this before starting live tracking
"""

import sys
import subprocess
from tracker_utils import print_opencv_info, get_available_trackers

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    print("-" * 50)
    
    packages = {
        "numpy": "NumPy",
        "pandas": "Pandas",
        "cv2": "OpenCV",
        "scipy": "SciPy",
        "matplotlib": "Matplotlib",
    }
    
    failed = []
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✓ {name:<20} OK")
        except ImportError as e:
            print(f"✗ {name:<20} FAILED: {e}")
            failed.append(name)
    
    return len(failed) == 0, failed

def test_local_modules():
    """Test if local modules can be imported"""
    print("\nTesting local modules...")
    print("-" * 50)
    
    modules = [
        "detection",
        "plotting",
        "tracker",
        "experiment_config",
        "liveTrack",
    ]
    
    failed = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module:<30} OK")
        except ImportError as e:
            print(f"✗ {module:<30} FAILED: {e}")
            failed.append(module)
    
    return len(failed) == 0, failed

def test_opencv_trackers():
    """Test if OpenCV trackers are available"""
    print("\nTesting OpenCV trackers...")
    print("-" * 50)
    
    import cv2
    from tracker_utils import get_available_trackers
    
    available = get_available_trackers()
    
    if available:
        for tracker in available:
            print(f"✓ {tracker:<20} OK")
        return True, []
    else:
        print("✗ No trackers available")
        return False, ["All trackers"]

def main():
    print("=" * 50)
    print("PENDULUM TRACKING SYSTEM - INSTALLATION CHECK")
    print("=" * 50)
    print()
    
    # Print OpenCV info
    print("OpenCV Information:")
    print("-" * 50)
    print_opencv_info()
    
    # Test imports
    imports_ok, failed_imports = test_imports()
    
    # Test local modules
    modules_ok, failed_modules = test_local_modules()
    
    # Test trackers
    trackers_ok, failed_trackers = test_opencv_trackers()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    
    if imports_ok and modules_ok and trackers_ok:
        print("✓ ALL TESTS PASSED!")
        print("\nYou can now run:")
        print("  python menu.py")
        print("or")
        print("  python test_integration.py --mode live --experiment 1")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("\nFailed packages:", failed_imports or "None")
        print("Failed modules:", failed_modules or "None")
        print("Failed trackers:", failed_trackers or "None")
        print("\nPlease run:")
        print("  pip install --upgrade -r requirements.txt")
        print("\nIf the problem persists:")
        print("  pip uninstall opencv-python opencv-contrib-python")
        print("  pip install opencv-contrib-python==4.10.0.106")
        return 1

if __name__ == "__main__":
    sys.exit(main())
