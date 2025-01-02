import cv2
import cv2.aruco as aruco
import numpy as np
import math

# --- PARAMETERS ---
focal_length = 2900.00  # px 
max_angle = 290      # deg 

tag_size = 2.5  # Adjust based on real tag size



# --- INIT CAM ---
cap = cv2.VideoCapture(0)  # Open cam
if not cap.isOpened():  # Check cam
    print("Err cam.")  # Cam failed
    exit()

print("Press 'q' to quit.")  # Quit msg

while True:
    # Read img from cam
    ret, frame = cap.read()
    if not ret:
        print("Error video.")  # Video issue
        break

    # Convert to grayscale (tag detect)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect tags (Aruco lib)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    corners, ids, _ = aruco.detectMarkers(gray_frame, aruco_dict)

    # Screen dims + ref pts
    h, w, _ = frame.shape
    bottom_center = (w // 2, h - 10)  # Red pt at bottom center

    # Draw vertical mid-line
    cv2.line(frame, (w // 2, 0), (w // 2, h), (255, 0, 0), 1)  # Thin blue line

    # Red pt at bottom center
    cv2.circle(frame, bottom_center, 5, (0, 0, 255), -1)

    # Init angle to display
    final_angle = 0.0

    if ids is not None:  # If tags detected
        # Draw detected tags
        aruco.drawDetectedMarkers(frame, corners, ids)

        # Get tag centers
        markers = []
        for corner, marker_id in zip(corners, ids.flatten()):
            center_x = int(corner[0][:, 0].mean())  # Avg X
            center_y = int(corner[0][:, 1].mean())  # Avg Y
            markers.append((marker_id, (center_x, center_y)))  # Store ID + (X, Y)

        # Sort tags by X position
        markers.sort(key=lambda x: x[1][0])  # Ascending X

        # Detect rows
        rows = []  # Store rows
        current_row = []  # Current row
        for i, (marker_id, position) in enumerate(markers):
            if not current_row:  # 1st tag in row
                current_row.append((marker_id, position))
            else:
                # Dist to prev tag
                prev_position = current_row[-1][1]
                distance_x = abs(position[0] - prev_position[0])

                # Check if spacing is ok
                if 10 <= distance_x <= 200:  # Spacing valid
                    current_row.append((marker_id, position))  # Add tag
                else:  # New row
                    if len(current_row) == 4:  # Complete row
                        rows.append(current_row)
                    current_row = [(marker_id, position)]

        # Add last row if valid
        if len(current_row) == 4:
            rows.append(current_row)

        # Process rows (draw + calc)
        for row in rows:
            # Get min/max coords
            x_coords = [pos[0] for _, pos in row]
            y_coords = [pos[1] for _, pos in row]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords) - 20, max(y_coords) + 20

            # Green rect for row
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Diagonal center
            diag_center = ((x_min + x_max) // 2, (y_min + y_max) // 2)
            cv2.circle(frame, diag_center, 5, (0, 0, 255), -1)  # Red diag center

            # Orange line to diag center
            cv2.line(frame, bottom_center, diag_center, (0, 165, 255), 2)  # Orange line

            # Calc angle (raw)
            delta_x = diag_center[0] - bottom_center[0]
            delta_y = bottom_center[1] - diag_center[1]
            angle = math.degrees(math.atan2(delta_x, delta_y))  # Angle (uncalibrated)

            # Scale angle using FOV
            real_angle = (angle / (w / 2)) * (max_angle / 2)  # Calibrated angle
            final_angle = real_angle  # Save angle for display

            # Calc distance to camera
            pixel_width = x_max - x_min
            if pixel_width > 0:
                distance_cam = (tag_size * focal_length) / pixel_width
                cv2.putText(frame, f"Dist: {distance_cam:.2f} cm", (x_min, y_max + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)  # Blue text

            # Show spacing between extremes
            spacing = x_max - x_min
            cv2.putText(frame, f"Spacing: {spacing}px", (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)  # Blue text

    # Show angle at bottom (orange, bold)
    cv2.putText(frame, f"Angle: {final_angle:+.1f} deg", (10, h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    # Show img
    cv2.imshow("ArUco Navigation", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# close
cap.release()
cv2.destroyAllWindows()
