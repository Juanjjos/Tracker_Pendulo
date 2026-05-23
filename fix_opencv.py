#!/usr/bin/env python3
"""
Fix OpenCV installation issues
Run this if you're getting tracker errors
"""

import subprocess
import sys
import os

print("=" * 70)
print("🔧 OpenCV Installation Fix")
print("=" * 70)

print("\nThis script will:")
print("  1. Uninstall all OpenCV versions")
print("  2. Reinstall opencv-contrib-python correctly")
print("  3. Verify trackers are working")

confirm = input("\nDo you want to continue? (y/n): ").strip().lower()
if confirm != "y":
    print("Cancelled.")
    sys.exit(0)

print("\n" + "=" * 70)
print("Step 1: Uninstalling old OpenCV versions...")
print("=" * 70)

packages_to_remove = [
    "opencv-python",
    "opencv-contrib-python",
    "opencv-python-headless",
    "opencv-contrib-python-headless",
]

for package in packages_to_remove:
    print(f"\nRemoving {package}...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", package, "-y"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"  ✓ {package} removed")
    else:
        if "not installed" in result.stderr.lower():
            print(f"  - {package} was not installed")
        else:
            print(f"  ⚠ Warning: {result.stderr}")

print("\n" + "=" * 70)
print("Step 2: Installing opencv-contrib-python...")
print("=" * 70)

print("\nInstalling opencv-contrib-python==4.10.0.106...")
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "--no-cache-dir", 
     "opencv-contrib-python==4.10.0.106"],
    capture_output=False,
    text=True
)

if result.returncode != 0:
    print("\n✗ Installation failed!")
    print("Try installing manually:")
    print("  pip install --upgrade --no-cache-dir opencv-contrib-python")
    sys.exit(1)

print("\n" + "=" * 70)
print("Step 3: Verifying installation...")
print("=" * 70)

try:
    import cv2
    print(f"\n✓ OpenCV {cv2.__version__} installed successfully")
    
    from tracker_utils import get_available_trackers
    trackers = get_available_trackers()
    
    if trackers:
        print(f"✓ Available trackers: {', '.join(trackers)}")
        print("\n✅ OpenCV installation fixed!")
        print("\nYou can now run:")
        print("  python menu.py")
    else:
        print("✗ No trackers available")
        print("\nTry running check_installation.py for more details")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("Please try installing manually:")
    print("  pip install opencv-contrib-python==4.10.0.106")
    sys.exit(1)

print("\n" + "=" * 70)
