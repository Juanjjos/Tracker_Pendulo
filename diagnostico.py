#!/usr/bin/env python3
"""
Quick Diagnostic Script for Pendulum Tracking System
Run this to diagnose OpenCV issues
"""

import sys
import os

print("=" * 70)
print("🔧 PENDULUM TRACKING SYSTEM - QUICK DIAGNOSTICS")
print("=" * 70)

print("\n1. Checking Python version...")
print(f"   Python: {sys.version}")
print(f"   Executable: {sys.executable}")

print("\n2. Checking OpenCV installation...")
try:
    import cv2
    print(f"   ✓ OpenCV {cv2.__version__} installed")
    print(f"   Location: {cv2.__file__}")
except ImportError as e:
    print(f"   ✗ OpenCV not found: {e}")
    print("\n   Fix: pip install opencv-contrib-python==4.10.0.106")
    sys.exit(1)

print("\n3. Checking tracker availability...")
try:
    from tracker_utils import get_available_trackers, print_opencv_info
    available = get_available_trackers()
    
    if available:
        print(f"   ✓ Available trackers: {', '.join(available)}")
    else:
        print(f"   ✗ No trackers available")
        print("\n   Detailed info:")
        print_opencv_info()
        
        print("\n   FIX: Try one of these:")
        print("   1. pip uninstall opencv-python opencv-contrib-python -y")
        print("   2. pip install opencv-contrib-python==4.10.0.106")
        print("   3. python check_installation.py")
        sys.exit(1)
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n4. Checking required modules...")
required_modules = [
    ("numpy", "NumPy"),
    ("pandas", "Pandas"),
    ("scipy", "SciPy"),
    ("matplotlib", "Matplotlib"),
]

all_ok = True
for module_name, display_name in required_modules:
    try:
        __import__(module_name)
        print(f"   ✓ {display_name}")
    except ImportError:
        print(f"   ✗ {display_name} not installed")
        all_ok = False

if not all_ok:
    print("\n   Fix: pip install -r requirements.txt")
    sys.exit(1)

print("\n5. Checking local modules...")
local_modules = [
    "detection",
    "plotting",
    "tracker",
    "experiment_config",
    "liveTrack",
]

for module in local_modules:
    try:
        __import__(module)
        print(f"   ✓ {module}.py")
    except ImportError as e:
        print(f"   ✗ {module}.py: {e}")
        all_ok = False

if not all_ok:
    print("\n   Fix: Make sure all Python files are in this directory")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL CHECKS PASSED - System is ready!")
print("=" * 70)

print("\nYou can now run:")
print("  1. python menu.py              (Interactive menu)")
print("  2. python test_integration.py --mode live --experiment 1")
print("  3. python liveTrack.py --source 0")

print("\n" + "=" * 70)
