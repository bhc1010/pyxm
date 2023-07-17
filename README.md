# SAM 9000 (Scanning Tunneling Microscope AutoMator) 

![alt text](https://github.com/bhc1010/stm_automator/blob/master/sam_9000.PNG)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation (from source)](#installation-from-source)
  - [Installation (as an executable)](#installation-as-an-executable)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)


## Introduction

Congratulations on purchasing your brand new SAM 9000! This application is an advanced Scanning Tunneling Microscope (STM) control and management system, enabling users to perform various imaging and spectroscopy tasks with ease and precision. The application provides an intuitive graphical user interface (GUI) and leverages the power of PySide6 library to ensure a smooth and responsive user experience.

The name "SAM 9000" pays homage to HAL 9000, the iconic sentient computer from the movie "2001: A Space Odyssey." Rest assured, SAM 9000 will not exhibit any of HAL's problematic tendencies – it's here to enhance your STM experiments!

## Features

- Connect to an STM device using TCP/IP sockets, ensuring efficient communication and control.
- Control STM parameters such as bias voltage, scan area, line time, and more, with easy-to-use sliders and input fields.
- Capture STM images with customizable scan size, position, and bias, providing precise control over experimental parameters.
- Perform scanning tunneling spectroscopy (STS) with adjustable start, stop, and step values, enabling detailed material characterization.
- Execute tasks sequentially or simultaneously, allowing for versatile experimentation and efficient workflow management.
- Background task execution using worker threads ensures that the GUI remains responsive even during resource-intensive tasks.
- Custom GUI elements provide clear visualization and intuitive interaction, enhancing the user experience.
- Stylish UI with custom styling using QDarkTheme, ensuring an aesthetic and enjoyable experience for users.

## Getting Started

### Prerequisites

To run the SAM 9000 application, you need the following dependencies installed on your system:

- Python (version 3.11 or higher)
- PySide6
- numpy
- pyqtdarktheme

### Installation (from source)

1. Clone this repository to your local machine:
```console
git clone https://github.com/bhc1010/sam9000

```
2. Change to the project directory:
```console
cd sam9000
```
3. Install the required Python packages using pip:
```console
pip install -r requirements.txt
```

4. Launch the STM application by running main.py

5. The application's GUI will appear, allowing you to connect to the STM device and perform various tasks.

### Installation (as an executable)

1. Download the latest release of SAM 9000 from the [Releases](https://github.com/bhc1010/sam9000/releases) section.

2. Extract the downloaded archive to a location of your choice.

3. Run the SAM 9000 executable appropriate for your operating system.

4. The application's GUI will appear, allowing you to connect to the STM device and perform various tasks.


## Customization

You have the flexibility to customize the SAM 9000 application to meet the specific requirements of your STM device. Here are some ways to tailor the application to your needs:

- **Custom STM Commands**: To accommodate the specific commands and syntax used by your STM device, the application allows you to edit the `stm_commands.json` JSON file. In this JSON file, you can define the custom commands required to interact with your STM. The application will then read this file and use the provided commands when communicating with the STM device.
  
Example of `stm_commands.json` for the RHK PanScanFreedom via the R9:

```json
{
  "set_bias": "SetSWParameter, STM Bias, Value",
  "set_setpoint": "SetSWParameter, STM Set Point, Value",
  "set_scansize": "SetSWParameter, Scan Area Window, Scan Area Size",
  "set_xoffset":   "SetSWParameter, Scan Area Window, X Offset",
  "set_yoffset":   "SetSWParameter, Scan Area Window, Y Offset"
  "etc": "..."
}
```
**If running from source:**
- Extend the functionality of the STM device by adding new methods to the `STM` class in `stm.py`.
- Implement additional task types by extending the `TaskType` enum in `taskdata.py`.
- Customize the styling of the application by editing the `style.css` file in the `src/ui/style/` directory.

**If running as an executable:**
- Custom STM commands: Coming soon! In a future update, you will be able to customize the STM commands used by the application by editing the `stm_commands.json` file. This will allow you to adapt the application to fit the specific TCP/IP protocols of your particular STM device. Stay tuned for this exciting feature!



## Contributing

We welcome contributions to the STM application! If you find a bug, have an enhancement idea, or want to add new features, please follow these steps:

1. Fork the repository to your GitHub account.
2. Create a new branch with a descriptive name for your changes.
3. Make your changes and test thoroughly.
4. Commit your changes and push them to your forked repository.
5. Create a pull request, explaining your changes in detail.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please feel free to contact the project maintainers:

- Ben Campbell - [ben.campbell@unh.edu](mailto:ben.campbell@unh.edu)

We hope you find SAM 9000 to be a valuable tool for your STM experiments! Happy scanning, and remember, "I'm sorry, I can't do that" is not a response you'll get from SAM 9000! 😄🚀
