# Open Score OCR

![Open Score OCR in action](https://via.placeholder.com/800x400.png?text=Open+Score+OCR+Demo) <!-- Replace with actual screenshot or demo image -->

## Overview

Open Score OCR is a Python-based tool designed to extract text from user-defined regions in a live video feed and save each region's text to separate files (`box1.txt`, `box2.txt`, etc.) in an `outputs` subfolder. It supports multiple video sources, including webcams and Blackmagic devices (e.g., DeckLink or WebPresenter via USB/Thunderbolt), and updates the text files at a user-specified interval (1, 5, or 10 seconds). Each region is labeled with a number in the top-right corner for easy identification. The extracted text is ideal for integration with vMix or similar programs for real-time display, making it perfect for applications like live scoring or data overlays in video production.

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
   python3 -m pip install --user opencv-python==4.10.0 pytesseract==0.3.13
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
   python -m pip install --user opencv-python==4.10.0 pytesseract==0.3.13
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

6. **Tesseract Path (if needed)**:
   If Tesseract is not found, edit `open_score_ocr.py` to uncomment and set:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Both Platforms

- **Python**: Version 3.8 or higher is required (3.10 recommended).
- **Blackmagic Devices**: Ensure the device is connected and detected in Blackmagic Desktop Video Setup.

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/mhankosky/OpenScoreOCR.git
   cd OpenScoreOCR
   ```

2. Follow the platform-specific prerequisites above to install dependencies.

3. Ensure `open_score_ocr.py` is in the project directory.

## Usage

1. Run the script:
   ```bash
   python open_score_ocr.py  # Use python3 on macOS
   ```

2. **Select Refresh Rate**:
   - Enter `1`, `2`, or `3` for 1, 5, or 10 seconds, respectively.

3. **Select Video Source**:
   - **Option 1**: Default webcam (index 0).
   - **Option 2**: Specify a webcam index (e.g., 1, 2).
   - **Option 3**: Blackmagic device (DeckLink/WebPresenter). Provide device number (default 0) and connection type (e.g., HDMI=1).

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

1. Add a **Text** input in vMix for each output file (e.g., `outputs/box1.txt`).
2. Set the source to the file path (use full path on Windows, e.g., `C:\path\to\OpenScoreOCR\outputs\box1.txt`).
3. Enable **Auto Update** in vMix and set the interval to match the script's refresh rate (1, 5, or 10 seconds).
4. Use separate Text inputs for each box to display multiple text regions.

## Troubleshooting

- **Tesseract Not Found**:
  - **Windows**: Ensure Tesseract is in your PATH (`set PATH=%PATH%;C:\Program Files\Tesseract-OCR`) or set `pytesseract.pytesseract.tesseract_cmd` in the script.
  - **macOS**: Verify `tesseract --version`. Reinstall with `brew install tesseract` if needed.

- **OpenCV ModuleNotFoundError**:
  - Run `python -m pip install --user opencv-python==4.10.0` (use `python3` on macOS).
  - Check Python environment: `python -m pip list` (or `python3`) and ensure `opencv-python` is listed.
  - Verify Python version: `python --version` (or `python3`). Must be 3.8+.

- **Blackmagic Device Fails**:
  - Verify the device is detected in Blackmagic Desktop Video Setup.
  - Check GStreamer support:
    ```bash
    python -c "import cv2; print(cv2.getBuildInformation())" | findstr GStreamer  # Windows
    python -c "import cv2; print(cv2.getBuildInformation())" | grep GStreamer  # macOS
    ```
    Must show `YES`.
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
    - **Windows**: Use CMake GUI or follow OpenCV build guides with GStreamer enabled (see [OpenCV documentation](https://docs.opencv.org/master/d7/d9f/tutorial_gstreamer.html)).
  - Test with a webcam (option 1) to isolate issues.

- **Poor OCR Accuracy**:
  - Ensure the video feed has clear, high-contrast, well-lit text.
  - Adjust box placement to tightly encompass text areas.
  - Consider preprocessing images (e.g., increasing contrast) in the script if needed.

- **Output Files Not Created**:
  - Check the `outputs` folder in the script directory.
  - Ensure write permissions: `chmod -R u+w outputs` (macOS) or check folder permissions (Windows).
  - Verify the script is running in the correct directory (`cd OpenScoreOCR`).

- **vMix Not Updating**:
  - Ensure the file path in vMix is correct (use absolute paths on Windows).
  - Verify Auto Update is enabled and matches the refresh rate.
  - Check that the `outputs` folder is accessible to vMix (e.g., not in a restricted directory).

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
  - Open an issue at [mhankosky/OpenScoreOCR](https://github.com/mhankosky/OpenScoreOCR/issues).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit issues or pull requests to improve the tool. For major changes, open an issue first to discuss the proposed changes.

## Contact

For support or feature requests, create an issue on the GitHub repository: [mhankosky/OpenScoreOCR](https://github.com/mhankosky/OpenScoreOCR).
