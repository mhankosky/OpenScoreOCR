# Open Score OCR
Tested on MacOS Tahoe 26
Description: This is a tool that takes a video feed from a camera source (default webcam, specific webcam index, or Blackmagic DeckLink/WebPresenter via USB/Thunderbolt)
and extracts text from user-defined regions, writing each region's text to a separate file (box1.txt, box2.txt, etc.) in the 'outputs' subfolder at a user-set interval (1, 5, or 10 seconds).
This allows the extracted text to be imported into vMix or other programs for real-time display.

# Instructions:
1. Install Homebrew (if not already installed):
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   Then add to PATH (Apple Silicon):
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   (For Intel Macs, replace /opt/homebrew with /usr/local)
2. Install system dependencies:
   brew install tesseract gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
3. Install Python packages:
   python3 -m pip install --user opencv-python pytesseract
4. Verify installations:
   tesseract --version
   python3 -c "import cv2; print(cv2.__version__)"
   python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
   python3 -c "import cv2; print(cv2.getBuildInformation())" | grep GStreamer  # Ensure GStreamer: YES
5. Ensure Blackmagic Desktop Video software is installed for DeckLink/WebPresenter (available at https://www.blackmagicdesign.com/products/decklink/downloads).
6. Run this script: python3 open_score_ocr.py
7. Follow prompts to select refresh rate (1, 5, or 10 seconds) and video source (default webcam, specific webcam index, or Blackmagic device).
8. Click and drag to draw boxes over text areas in the video feed; each box is labeled with a number in the top-right corner.
9. Press 'd' when done drawing boxes to start text extraction.
10. Text from each box is written to 'outputs/box1.txt', 'outputs/box2.txt', etc., at the selected interval, suitable for import into vMix or similar programs.
11. Press 'q' to quit.
