import cv2
from plotting import fit_amplitude
from detection import detect_object
import sys, pandas as pd, math, argparse
from scipy.signal import savgol_filter

def live_track(tracker, video_src, hilo_length_cm=30, area_condition="sin_hojas"):
    """
    Live track pendulum using webcam or video file.
    
    Args:
        tracker: OpenCV tracker object
        video_src: Video source (0 for webcam, or path to video file)
        hilo_length_cm: Length of the string in cm. Default is 30.
        area_condition: Experimental condition - "sin_hojas" or "con_hojas". Default is "sin_hojas".
    """

    roi = detect_object()

    cap = cv2.VideoCapture(int(video_src) if isinstance(video_src, str) and video_src.isdigit() else video_src)

    # Exit if video not opened.
    if not cap.isOpened():
        print("Could not open video")
        sys.exit()

    # Before starting the tracking, let the user pick a equilibrium point as origin
    origin = None

    def select_point(event, x, y, flags, param):
        nonlocal origin
        if event == cv2.EVENT_LBUTTONDOWN:
            origin = (x, y)
            print(f"Equilibrium Point set at: X = {x}, Y = {y}")

    ret, frame = cap.read()
    if not ret:
        print('Cannot read video file')
        sys.exit()

    # Limit window size, resize frame if necessary
    frame_height, frame_width = frame.shape[:2]
    cv2.namedWindow("Select Equilibrium Point", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Select Equilibrium Point", min(frame_width, 800), min(frame_height, 600))

    cv2.setMouseCallback("Select Equilibrium Point", select_point)

    while origin is None:
        cv2.imshow("Select Equilibrium Point", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit() 

    cv2.destroyWindow("Select Equilibrium Point")

    # Calculate L_px (string length in pixels) from ROI
    x_roi, y_roi, w_roi, h_roi = map(int, roi)
    mass_y_initial = y_roi + h_roi // 2
    L_px = abs(origin[1] - mass_y_initial)  # Vertical distance is the string length
    
    if L_px < 10:
        print("Warning: L_px is very small. Ensure ROI was selected correctly.")
        L_px = 100  # Default fallback

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, roi)

    position_log = []
    current_frame = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        ok, bbox = tracker.update(frame)
        current_time = (current_frame / fps)
        
        if ok:
            x, y, w, h = map(int, bbox)
            p1 = (x, y)
            p2 = (x + w, y + h)
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            center_x = x + w // 2
            center_y = y + h // 2

            # Calculate displacement from equilibrium point
            adj_x = center_x - origin[0]
            adj_y = origin[1] - center_y  # CORRECTED: use origin[1] for y coordinate

            # Convert pixel displacement to angle using θ = arcsin(x_c / L_px)
            if L_px > 0:
                angle_rad = math.asin(adj_x / L_px) if abs(adj_x / L_px) <= 1 else 0
                angle = math.degrees(angle_rad)
            else:
                angle = 0
            
            if current_frame % 5 == 0:
                position_log.append([round(current_time, 3), adj_x, adj_y, round(angle, 3)])

            # Display information on screen
            cv2.putText(frame, f"Time: {current_time:.2f}s, X: {adj_x:.2f}px, Y:{adj_y:.2f}px", 
                       (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 170, 50), 2)
            cv2.putText(frame, f"Angle: {angle:.2f}°, L_px: {L_px}", 
                       (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 170, 50), 2)

        else:
            cv2.putText(frame, "Tracking failure detected", (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            
        # Display result
        cv2.namedWindow("Tracking", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Tracking", min(frame_width, 800), min(frame_height, 600))
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        current_frame += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    # Save data to CSV
    df = pd.DataFrame(position_log, columns=["Time(s)", "X", "Y", "Angle(deg)"])
    df.to_csv("live_track_output.csv", index=False)
    print(f"Position data saved to live_track_output.csv")

    # Generate plot with fit_amplitude
    png_path = "live_track_output.png"
    metadata_path = "live_track_metadata.csv"
    fit_amplitude(df, output_path=png_path, 
                 hilo_length_cm=hilo_length_cm,
                 area_condition=area_condition,
                 metadata_output_path=metadata_path)
    print(f"Amplitude plot saved to {png_path}")
    print(f"Metadata saved to {metadata_path}")
    print(f"Amplitude plot saved.") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify tracker and video source.")

    parser.add_argument(
        '--tracker',
        type=str,
        help='Please use capitalized name, see README.md',
        default="KCF"
    )

    parser.add_argument(
        '--source',
        type=str,
        default="0",
        help='Video source, webcam is usually 0'
    )

    args = parser.parse_args()

    trackers = {
        "CSRT": cv2.legacy.TrackerCSRT_create,
		"KCF": cv2.legacy.TrackerKCF_create,
		"BOOSTING": cv2.legacy.TrackerBoosting_create,
		"MIL": cv2.legacy.TrackerMIL_create,
		"TLD": cv2.legacy.TrackerTLD_create,
		"MEDIANFLOW": cv2.legacy.TrackerMedianFlow_create,
		"MOSSE": cv2.legacy.TrackerMOSSE_create
    }

    tracker = trackers[args.tracker]()

    print(f"Using tracker: {args.tracker}")
    print(f"Using video source: {args.source}")

    live_track(tracker, args.source)