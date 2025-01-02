# **ArUco-Based Structure Detection and Navigation System**  

This project is part of the **Eurobot Competition**, where our **constructor robot** is designed to detect and interact with structures composed of **four columns and a top plank**. Each column has an **ArUco marker** for identification.  

The robot uses a **camera** to identify a structure by grouping **four ArUco markers**. It then calculates the **center point, distance**, and **angle** needed to approach the structure based on the detected markers.  

---

## **1. Features**  

- **Marker Detection**: Detects ArUco markers using **OpenCV** and identifies valid structures.  
- **Position Estimation**: Calculates the **center point** of the structure and marks it with a **rectangle**.  
- **Distance Measurement**: Estimates the **distance** using marker size and camera parameters.  
- **Angle Calculation**: Determines the **orientation angle** based on marker positions within the camera frame.  
- **Real-Time Feedback**: Displays detected markers, positions, angles, and distances directly on the camera feed.  

---

## **2. Setup and Calibration**  

**Camera Calibration** was initially attempted using:  
- **OpenCV Matrix Calibration**  
- **Online Calibration Tool**: [calibdb.net](https://www.calibdb.net)  

However, the results were inconsistent. Instead, **manual calibration** was used by empirically tuning:  

Although this approach is **not ideal**, it proved to be **very accurate** for the application.  

---

## **3. Challenges and Limitations**  

1. **Stability Issues**:  
   - Small **vibrations** during motion affect detection reliability.  
   - The robot must **stop periodically** (for ~1 second) to take stable measurements.  

2. **Calibration Tradeoff**:  
   - Manual calibration is **not scalable** for other cameras and needs reconfiguration if hardware changes.  

---

## **4. Dependencies and Libraries**  

This project uses the following Python libraries:  
- **OpenCV** (`cv2`): Image processing and ArUco detection.  
- **Numpy** (`np`): Mathematical operations and matrix handling.  
- **Math**: Angle and distance calculations.  

---

## **5. How It Works**  

### **Initialization**  
1. Open camera (`cv2.VideoCapture`).  
2. Display a **vertical centerline** and a **bottom reference point**.  

### **Marker Detection**  
3. Convert frames to **grayscale** for easier marker recognition.  
4. Detect markers using **ArUco predefined dictionaries**.  
5. Identify markers by **IDs** and group them into **rows** based on position.  

### **Structure Validation**  
6. Ensure groups have **4 markers** arranged horizontally.  
7. Draw **bounding rectangles** around detected structures.  

### **Calculations**  
8. Compute:
   - **Distance**: Using marker size and camera parameters.  
   - **Angle**: Based on horizontal position relative to the camera center and the distance.  

10. Display computed values on the screen (real-time feedback).  

---


## **6. Next Steps**  

- **Optimize Calibration**: Rework calibration with a proper method once the **final camera hardware** is installed.  
- **Improve Stability**: Introduce a **motion stabilization algorithm** to reduce the impact of vibrations.  

All contributions are welcome