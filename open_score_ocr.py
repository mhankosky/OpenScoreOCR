import cv2
import pytesseract
import time
import os
import sys
import platform

# Open Score OCR
# Description: This is a tool that takes a video feed from a camera source (default webcam, specific webcam index, or Blackmagic DeckLink/WebPresenter via USB/Thunderbolt)
# and extracts text from user-defined regions, writing each region's text to a separate file (box1.txt, box2.txt, etc.) in the 'outputs' subfolder at a user-set interval (1, 5, or 10 seconds).
# Each box is labeled with a number in the top-right corner. The extracted text can be imported into vMix or other programs for real-time display.
# This tool is compatible with both macOS and Windows.

# Instructions for macOS:
# 1. Install Homebrew (if not already installed):
#    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
#    Then add to PATH (Apple Silicon):
#    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
#    eval "$(/opt/homebrew/bin/brew shellenv)"
#    (For Intel Macs, replace /opt/homebrew with /usr/local)
# 2. Install system dependencies:
#    brew install tesseract gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
# 3. Install Python packages:
#    python3 -m pip install --user opencv-python pytesseract
# 4. Verify installations:
#    tesseract --version
#    python3 -c "import cv2; print(cv2.__version__)"
#    python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
#    python3 -c "import cv2; print(cv2.getBuildInformation())" | grep GStreamer  # Ensure GStreamer: YES
# 5. Ensure Blackmagic Desktop Video software is installed for DeckLink/WebPresenter (download from https://www.blackmagicdesign.com/products/decklink/downloads).

# Instructions for Windows:
# 1. Install Chocolatey (if not already installed, run in an Administrator PowerShell):
#    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
# 2. Install system dependencies using Chocolatey (in Administrator Command Prompt or PowerShell):
#    choco install tesseract gstreamer gstreamer-devel -y
#    Alternatively, download and install manually:
#    - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki (add to PATH, e.g., C:\Program Files\Tesseract-OCR)
#    - GStreamer: https://gstreamer.freedesktop.org/download/ (install both runtime and development packages, e.g., gstreamer-1.0-x86_64-<version>.msi and gstreamer-1.0-devel-x86_64-<version>.msi)
# 3. Install Python packages (in Command Prompt or PowerShell):
#    python -m pip install --user opencv-python pytesseract
# 4. Verify installations:
#    tesseract --version
#    python -c "import cv2; print(cv2.__version__)"
#    python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
#    python -c "import cv2; print(cv2.getBuildInformation())" | findstr GStreamer  # Ensure GStreamer: YES
# 5. Ensure Blackmagic Desktop Video software is installed for DeckLink/WebPresenter (download from https://www.blackmagicdesign.com/products/decklink/downloads).
# 6. If Tesseract is not found by pytesseract, set the path explicitly in this script (uncomment and adjust):
#    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Run the script:
#    python open_score_ocr.py
# 1. Follow prompts to select refresh rate (1, 5, or 10 seconds) and video source (default webcam, specific webcam index, or Blackmagic device).
# 2. Click and drag to draw boxes over text areas in the video feed; each box is labeled with a number in the top-right corner.
# 3. Press 'd' when done drawing boxes to start text extraction.
# 4. Text from each box is written to 'outputs/box1.txt', 'outputs/box2.txt', etc., at the selected interval, suitable for import into vMix or similar programs.
# 5. Press 'q' to quit.

# Uncomment and set Tesseract path for Windows if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variables
drawing = False
ix, iy = -1, -1
boxes = []  # List of boxes: each is (x1, y1, x2, y2)
img = None
mode = 'draw'  # 'draw' or 'extract'
output_dir = 'outputs'

# Create outputs directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, boxes

    if mode != 'draw':
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            # Draw all existing boxes with their numbers
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = box
                cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Add box number in top-right corner
                cv2.putText(img_copy, str(i+1), (x2-15, y1+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            # Draw the current box being drawn
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Open Score OCR', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        boxes.append((min(ix, x), min(iy, y), max(ix, x), max(iy, y)))
        # Redraw the frame with the new box
        img_copy = img.copy()
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Add box number in top-right corner
            cv2.putText(img_copy, str(i+1), (x2-15, y1+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow('Open Score OCR', img_copy)

# Prompt for refresh rate
print("\nSelect refresh rate for text extraction:")
print("1. 1 second")
print("2. 5 seconds")
print("3. 10 seconds")
refresh_choice = input("Enter choice (1/2/3): ")
if refresh_choice == '1':
    refresh = 1
elif refresh_choice == '2':
    refresh = 5
elif refresh_choice == '3':
    refresh = 10
else:
    print("Invalid choice, defaulting to 1 second.")
    refresh = 1

# Prompt for video source
print("\nSelect video source:")
print("1. Default webcam (index 0)")
print("2. Specify webcam index")
print("3. Blackmagic device (DeckLink/WebPresenter)")
source_choice = input("Enter choice (1/2/3): ")

if source_choice == '1':
    cap = cv2.VideoCapture(0)
elif source_choice == '2':
    try:
        index = int(input("Enter camera index: "))
        cap = cv2.VideoCapture(index)
    except ValueError:
        print("Invalid camera index. Defaulting to webcam (index 0).")
        cap = cv2.VideoCapture(0)
elif source_choice == '3':
    try:
        device_num = input("Enter device number (default 0): ")
        device_num = int(device_num) if device_num else 0
        connection = input("Enter connection (0=SDI, 1=HDMI, 2=Optical SDI, 3=Component, 4=Composite, 5=S-Video, default 1=HDMI): ")
        connection = int(connection) if connection else 1
        pipeline = f"decklinksrc device-number={device_num} connection={connection} mode=auto ! videoconvert ! video/x-raw,format=BGR ! appsink"
        cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    except ValueError:
        print("Invalid input for device number or connection. Defaulting to webcam (index 0).")
        cap = cv2.VideoCapture(0)
else:
    print("Invalid choice, defaulting to default webcam.")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source. Ensure the device is connected and drivers are installed.")
    print("For Blackmagic devices, verify Blackmagic Desktop Video is installed and GStreamer is enabled in OpenCV.")
    sys.exit(1)

cv2.namedWindow('Open Score OCR')
cv2.setMouseCallback('Open Score OCR', draw_rectangle)

print("Draw boxes by clicking and dragging. Each box will be numbered in the top-right corner. Press 'd' when done. Press 'q' to quit.")

while True:
    ret, img = cap.read()
    if not ret:
        print("Error: Failed to capture image. Check video source.")
        break

    if mode == 'draw':
        img_display = img.copy()
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            cv2.rectangle(img_display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Add box number in top-right corner
            cv2.putText(img_display, str(i+1), (x2-15, y1+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow('Open Score OCR', img_display)
    else:  # extract mode
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            try:
                crop = img[y1:y2, x1:x2]
                if crop.size == 0:
                    text = "Empty region"
                else:
                    text = pytesseract.image_to_string(crop).strip()
                # Write to individual file
                output_file = os.path.join(output_dir, f"box{i+1}.txt")
                try:
                    with open(output_file, 'w') as f:
                        f.write(text + '\n')
                except Exception as e:
                    print(f"Error writing to {output_file}: {e}")
            except Exception as e:
                print(f"Box{i+1} = Error: {str(e)}")

        print(f"Updated text files in {output_dir}/")

        # Display the frame with boxes and numbers
        img_display = img.copy()
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            cv2.rectangle(img_display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Add box number in top-right corner
            cv2.putText(img_display, str(i+1), (x2-15, y1+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.imshow('Open Score OCR', img_display)

        # Throttle to user-selected refresh rate
        time.sleep(refresh)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('d') and mode == 'draw':
        if boxes:
            mode = 'extract'
            print("Drawing done. Now extracting text...")
        else:
            print("No boxes drawn. Draw at least one box.")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"Final output written to {output_dir}/ (box1.txt, box2.txt, etc.)")