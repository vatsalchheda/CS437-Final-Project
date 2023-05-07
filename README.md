# Smart Shared Lock (RAVN) - IoT Application 

This repository contains the code for a smart shared lock IoT application. The application is designed for multiple users to access a shared space (such as a house, Airbnb, hotel, or bank) using a smart lock with a 4-step authorization process. Users can also register new authorized users to the system. In addition, the application provides a joint lock service, which requires multiple users to authenticate together to open the lock.


## Table of Contents

- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [File Metrics](#file-metrics)
- [Contributing](#contributing)


## Features

- 4-step authorization process:
  1. PIN entry (SHA-256 hashed on the backend)
  2. Face authorization (only authorized users can access the smart lock)
  3. Voice authentication (users must speak their password; converted to text, hashed, and matched against passwords in the config database)
  4. Biometric authorization (fingerprint matching)
- New user registration
- Activity reporting: If anyone tries to open the system and fails, a report of the activity is generated along with their photo and biometric fingerprint. This information is shared with all authenticated users via email.
- Joint lock service: Requires multiple users (n=2 or more) to authenticate together to open the lock.


## Installation and Setup

1. Clone the repository to your local machine: git clone https://github.com/vatsalchheda/CS437-Final-Project.git
2. Install the required dependencies: pip install -r requirements.txt
3. Integrate the sensors (web-camera, microphone, LED, biometric fingerprint) with raspberry pi 4
4. Configure the application by updating the `config.py` file with your own settings (e.g., emails, password hashes, SMTP server, API keys, etc.).
5. Run the main script: python driver.py


## Usage

1. Users can enter their PIN on the device or through a connected interface to initiate the authorization process.
2. The device will prompt users for face authorization. Users should position their face in front of the camera to proceed.
3. Users will be prompted for voice authentication. They should speak their password, and the application will convert their speech to text, hash it, and match it against the stored passwords in the config database.
4. Lastly, users must provide biometric authorization by placing their finger on the fingerprint sensor.
5. If all 4 steps are successfully completed, the user gains access to the shared space.
6. To register a new user, follow the on-screen instructions after successfully completing the authorization process.
7. For joint lock access, authorized users should follow the same 4-step authorization process one after the other within the allowed time window.


## Result
1. Adding a new user
![Email Alert: Adding new user](https://github.com/vatsalchheda/CS437-Final-Project/blob/master/Images/New%20User%20Email.png "Email Alert: Adding new user")
2. Intruder
![Email Alert: Intruder](https://github.com/vatsalchheda/CS437-Final-Project/blob/master/Images/Intruder%20Email.png "Email Alert: Intruder")


## File Metrics

- Total lines of code: 912
- Total files: 11 (excluding directories)
- Main languages used: Python


## Contributing

Pull requests are welcome. Please ensure that your changes do not break the existing functionality of the application.
