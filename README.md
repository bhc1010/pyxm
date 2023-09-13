<h1 align="center">
Atom 
</h1>

![atom app](https://github.com/bhc1010/atom/blob/master/sam_9000.PNG?raw=true)

Atom is a task management system for scanning tunneling microscopes written in Python 3.11, with the PySide6 GUI library.
It aims to provide a simple and intuitive interface for users to queue up multiple sets of images and spectroscopy tasks to preform in a user-defined order.
TCP/IP commands can be customized through a JSON file to fit the needs of any system.
**⚠️ Note: atom is currently in an experimental stage and only been tested on the RHK PanScan Freedom system. ⚠️**

## Features

- [x] Connect to an STM device using TCP/IP sockets
- [x] Fine-tuned control of STM parameters with easy-to-use input fields.
- [x] Simultaneous execution and creation of tasks allowing for versatile experimentation and efficient workflow management.
- [ ] Preview STM images inside scan area.
- [ ] Customize TCP/IP commands to accomodate the syntax used by the users STM controller.

## Installation

1. Download the latest release of SAM 9000 from the [Releases](https://github.com/bhc1010/sam9000/releases) section.

2. Extract the downloaded archive to a location of your choice.

3. Run the SAM 9000 executable appropriate for your operating system.

## Build from source

1. Clone the repository:
```console
git clone https://github.com/bhc1010/sam9000
```

2. Install the required Python packages using pip:
```console
cd atom
pip install -r requirements.txt
```

3. Run Atom:
```console
python src/main.py
```

## Customize STM Commands
Commands required to interact with your STM can be specified in the 'stm_commands.json' file.
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

## Contributing

We welcome contributions to Atom! If you find a bug, have an enhancement idea, or want to add new features, please follow these steps:

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
