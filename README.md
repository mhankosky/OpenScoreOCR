# Open Score OCR

## Overview
Open Score OCR is a Python-based tool that extracts text from user-defined regions in a live video feed and saves each region's text to separate files (`box1.txt`, `box2.txt`, etc.) in an `outputs` subfolder. The tool supports multiple video sources, including webcams and Blackmagic devices (e.g., DeckLink or WebPresenter via USB/Thunderbolt), and updates the text files at a user-specified interval (1, 5, or 10 seconds). Each region is labeled with a number in the top-right corner for easy identification. The extracted text is suitable for integration with vMix or similar programs for real-time display, making it ideal for applications like live scoring or data overlay in video production.

## Features
- **Video Sources**: Supports default webcam, specific webcam index, or Blackmagic DeckLink/WebPresenter.
- **Text Extraction**: Users draw rectangular regions ("boxes") on the video feed, and Tesseract OCR extracts text from each region.
- **Output**: Each box's text is written to a separate file (`outputs/box1.txt`, `outputs/box2.txt`, etc.) at the chosen refresh rate.
- **Box Labeling**: Each box displays its number (e.g., "1", "2") in the top-right corner during drawing and extraction.
- **Cross-Platform**: Compatible with macOS and Windows.
- **vMix Integration**: Text files can be imported into vMix for real-time display using Text inputs with Auto Update.

## Prerequisites
The tool requires specific software and libraries to function. Follow the platform-specific instructions below.

### macOS
1. **Homebrew** (package manager):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```
   (For Intel Macs, replace `/opt/homebrew` with `/usr/local`.)
2. **System Dependencies**:
   ```bash
   brew install tesseract gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
   ```
3. **Python Packages**:
   ```bash
   python3 -m pip install --user opencv-python pytesseract
   ```
4. **Blackmagic Desktop Video**: Download and install from [Blackmagic Design](https://www.blackmagicdesign.com/products/decklink/downloads) for DeckLink/WebPresenter support.
5. **Verify Installations**:
   ```bash
   tesseract --version
   python3 -c "import cv2; print(cv2.__version__)"
   python3 -c "import pytesseract; print(pytesseract.get_tesseract_version())"
   python3 -c "import cv2; print(cv2.getBuildInformation())" | grep GStreamer
   ```
   Ensure GStreamer output shows `YES`.

### Windows
1. **Chocolatey** (package manager, optional but recommended):
   Run in an Administrator PowerShell:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```
2. **System Dependencies**:
   Using Chocolatey (in Administrator Command Prompt or PowerShell):
   ```powershell
   choco install tesseract gstreamer gstreamer-devel -y
   ```
   Alternatively, manually install:
   - **Tesseract**: Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH (e.g., `C:\Program Files\Tesseract-OCR`).
   - **GStreamer**: Download runtime and development MSIs from [GStreamer Downloads](https://gstreamer.freedesktop.org/download/) (e.g., `gstreamer-1.0-x86_64-<version>.msi` and `gstreamer-1.0-devel-x86_64-<version>.msi`).
3. **Python Packages**:
   ```powershell
   python -m pip install --user opencv-python pytesseract
   ```
4. **Blackmagic Desktop Video**: Download and install from [Blackmagic Design](https://www.blackmagicdesign.com/products/decklink/downloads).
5. **Verify Installations**:
   ```powershell
   tesseract --version
   python -c "import cv2; print(cv2.__version__)"
   python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
   python -c "import cv2; print(cv2.getBuildInformation())" | findstr GStreamer
   ```
   Ensure GStreamer output shows `YES`.
6. **Tesseract Path (if needed)**: If Tesseract is not found, edit `open_score_ocr.py` to uncomment and set:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Both Platforms
- **Python**: Version 3.6 or higher is required.
- **Blackmagic Devices**: Ensure the device is connected and detected in Blackmagic Desktop Video Setup.

## Installation
1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd open-score-ocr
   ```
2. Follow the platform-specific prerequisites above to install dependencies.
3. Place `open_score_ocr.py` in your project directory.

## Usage
1. Run the script:
   ```bash
   python open_score_ocr.py  # Use python3 on macOS
   ```
2. **Select Refresh Rate**:
   - Choose 1, 2, or 3 for 1, 5, or 10 seconds, respectively.
3. **Select Video Source**:
   - Option 1: Default webcam (index 0).
   - Option 2: Specify a webcam index (e.g., 1, 2).
   - Option 3: Blackmagic device (DeckLink/WebPresenter). Provide device number and connection type (e.g., HDMI=1).
4. **Draw Boxes**:
   - Click and drag to draw rectangular regions over text areas in the video feed.
   - Each box is labeled with a number (e.g., "1", "2") in the top-right corner.
   - Draw multiple boxes as needed.
5. **Start Extraction**:
   - Press `d` when done drawing boxes to begin text extraction.
6. **Output**:
   - Text from each box is saved to `outputs/box1.txt`, `outputs/box2.txt`, etc., updated at the chosen interval.
7. **Quit**:
   - Press `q` to exit the program.

### vMix Integration
- Add a **Text** input in vMix for each output file (e.g., `outputs/box1.txt`).
- Set the source to the file path (use full path on Windows, e.g., `C:\path\to\open-score-ocr\outputs\box1.txt`).
- Enable "Auto Update" in vMix and set the interval to match the script's refresh rate (1, 5, or 10 seconds).
- Use separate Text inputs for each box to display multiple text regions.

## Troubleshooting
- **Tesseract Not Found**:
  - **Windows**: Ensure Tesseract is in your PATH or set `pytesseract.pytesseract.tesseract_cmd` in the script (see Windows instructions).
  - **macOS**: Verify `tesseract --version` works. Reinstall with `brew install tesseract` if needed.
- **OpenCV ModuleNotFoundError**:
  - Run `python -m pip install --user opencv-python` (use `python3` on macOS).
  - Check Python environment: `python -m pip list` (or `python3`) and ensure `opencv-python` is listed.
- **Blackmagic Device Fails**:
  - Verify the device is detected in Blackmagic Desktop Video Setup.
  - Check GStreamer support: `python -c "import cv2; print(cv2.getBuildInformation())" | findstr GStreamer` (Windows) or `grep GStreamer` (macOS). Must show `YES`.
  - If `NO`, rebuild OpenCV with GStreamer:
    - **macOS**:
      ```bash
      brew install cmake pkg-config libpng jpeg-turbo
      git clone https://github.com/opencv/opencv.git
      cd opencv
      mkdir build && cd build
      cmake -D WITH_GSTREAMER=ON -D CMAKE_BUILD_TYPE=RELEASE -D PYTHON3_EXECUTABLE=$(which python3) ..
      make -j$(sysctl -n hw.ncpu)
      sudo make install
      ```
    - **Windows**: Use CMake GUI or follow OpenCV build guides with GStreamer enabled.
  - Test with a webcam (option 1) to isolate issues.
- **Poor OCR Accuracy**:
  - Ensure the video feed has clear, high-contrast, well-lit text.
  - Adjust box placement to tightly encompass text areas.
- **Output Files Not Created**:
  - Check the `outputs` folder in the script directory.
  - Ensure write permissions in the directory.
- **General Issues**:
  - Share the output of:
    ```bash
    python -c "import cv2; print(cv2.__version__)"
    python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
    tesseract --version
    python -c "import cv2; print(cv2.getBuildInformation())" | findstr GStreamer  # Windows
    python -c "import cv2; print(cv2.getBuildInformation())" | grep GStreamer  # macOS
    ```
  - Include your platform (macOS/Windows), Python version (`python --version`), and any error messages.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please submit issues or pull requests to improve the tool. For major changes, open an issue first to discuss the proposed changes.

## Contact
For support or feature requests, create an issue on this GitHub repository.
