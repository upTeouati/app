# Screen Viewer Mobile App

A mobile application for viewing desktop screen shared by the desktop application.

## Features
- Real-time screen viewing
- WebSocket-based connection
- Simple and intuitive interface
- Connection status monitoring

## Building the APK

### Prerequisites
1. Install Buildozer:
```bash
pip install buildozer
```

2. Install required system packages (on Ubuntu/Debian):
```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
```

3. Initialize buildozer:
```bash
buildozer init
```

4. Build the APK:
```bash
buildozer android debug
```

The APK will be generated in the `bin` directory.

## Usage
1. Install the APK on your Android device
2. Enter the WebSocket URL provided by the desktop application
3. Click "Connect" to start viewing the shared screen
4. Click "Disconnect" to stop viewing

## Requirements
- Android 5.0 or higher
- Internet connection
- Desktop application running and sharing screen
