#!/usr/bin/env python3
"""
Quick Test - Verifica sin webcam
Corre todos los tests sin necesidad de hardware
"""

import sys

print("=" * 70)
print("⚡ QUICK TEST - Verificación sin Hardware")
print("=" * 70)

# Test 1: Imports básicos
print("\n[1/5] Imports básicos...")
try:
    import cv2
    import numpy as np
    import pandas as pd
    from scipy import signal
    import matplotlib
    print("  ✓ Todos los imports básicos OK")
except ImportError as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 2: tracker_utils
print("\n[2/5] Módulo tracker_utils...")
try:
    from tracker_utils import create_tracker, get_available_trackers, print_opencv_info
    trackers = get_available_trackers()
    if trackers:
        print(f"  ✓ Trackers disponibles: {', '.join(trackers)}")
    else:
        print("  ✗ No hay trackers disponibles")
        print("\n  FIX: pip install --upgrade opencv-contrib-python")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 3: Módulos locales
print("\n[3/5] Módulos locales...")
try:
    import detection
    import plotting
    import tracker
    import experiment_config
    import liveTrack
    print("  ✓ Todos los módulos locales OK")
except ImportError as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 4: Crear tracker
print("\n[4/5] Crear tracker...")
try:
    for tracker_name in trackers:
        t = create_tracker(tracker_name)
        print(f"  ✓ {tracker_name} tracker creado")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 5: Operaciones básicas
print("\n[5/5] Operaciones de datos...")
try:
    # Test numpy
    a = np.array([1, 2, 3])
    assert len(a) == 3
    
    # Test pandas
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    assert df.shape == (3, 2)
    
    # Test scipy
    from scipy.signal import find_peaks
    signal_data = np.sin(np.linspace(0, 10, 100))
    peaks, _ = find_peaks(signal_data)
    
    print("  ✓ Operaciones de datos OK")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ QUICK TEST PASSED - Sistema listo!")
print("=" * 70)

print("\nPuedes ejecutar:")
print("  python menu.py")
print("  python test_integration.py --mode live --experiment 1")

print("\n" + "=" * 70)
