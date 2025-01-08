# Subcam

This project aims to develop a remote-controlled submersible camera powered by a Raspberry Pi. The camera can be controlled over an Ethernet connection, allowing for real-time video streaming and motor control.

## Features

- **Real-time Video Streaming**: Stream live video from the submersible camera to a web interface.
- **Motor Control**: Remotely control the motors to navigate the submersible.
- **Web Interface**: User-friendly web interface for controlling the submersible and viewing the video feed.
- **PID Control**: Implement PID control for stable navigation.
- **WebSocket Communication**: Use WebSocket for real-time communication between the web interface and the Raspberry Pi.

## Project Structure - TODO: fill out when structure stabilizes


## Applicable Hardware

This section will be filled out later with details about the hardware components used in this project, including:

- Raspberry Pi model
- Camera module
- Motor controllers
- Sensors (e.g., IMU, magnetometer)
- Power supply
- Ethernet connection setup

## Getting Started

### Prerequisites

- Raspberry Pi with Raspbian OS
- Python 3.x
- Flask
- Flask-SocketIO
- pigpio library
- Adafruit BNO055 library

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/elec424-finalproject.git
    cd elec424-finalproject
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Start the pigpio daemon:
    ```sh
    sudo pigpiod
    ```

### Running the Application

1. Start the Flask application:
    ```sh
    python websocket/app.py
    ```

2. Open your web browser and navigate to `http://<raspberry_pi_ip>:5000` to access the control interface.

## Usage

- Use the web interface to control the submersible camera.
- Monitor the live video feed and adjust the motor controls as needed.
- Utilize the PID control for stable navigation.

## License

This project is licensed under the MIT License - see the [LICENSE](http://_vscodecontentref_/16) file for details.

## Acknowledgments

- John Reko, Ryan Pai, and Sean Hamilton for helping develop the PID control & driver
- Adafruit for the BNO055 sensor library
- Flask and Flask-SocketIO for the web framework and real-time communication
- pigpio library for GPIO control on the Raspberry Pi