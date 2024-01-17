<h1 align="center">
pyxm 
</h1>

![pyxm app](https://github.com/bhc1010/pyxm/assets/pyxm.png?raw=true)

pyxm is a task management system for scanning tunneling microscopes written in Python 3.11, with the PySide6 GUI library.
It aims to provide a simple and intuitive interface for users to queue up multiple sets of images and spectroscopy tasks to preform in a user-defined order.
TCP/IP commands can be customized through a JSON file to fit the needs of any system.
pyxm is designed to communicate with an already existing STM controller and cannot control an STM directly.

**⚠️ pyxm is currently in an experimental stage and only been tested on the RHK PanScan Freedom system. ⚠️**

## Features

- [x] Connect to an STM device using TCP/IP sockets
- [x] Fine-tuned control of STM parameters with easy-to-use input fields.
- [x] Simultaneous execution and creation of tasks allowing for versatile experimentation and efficient workflow management.
- [ ] Preview images from a task inside scan area.
- [ ] Save task sets for reuse or documentation.
- [ ] Customize TCP/IP commands to accomodate syntax used by the users STM controller.

## Build from source

1. Clone the repository:
```console
git clone https://github.com/bhc1010/sam9000
```

2. Install the required Python packages using pip:
```console
cd pyxm
pip install -r requirements.txt
```

3. Run pyxm:
```console
python src/main.py
```

## Custom STM commands
Commands required to interact with your STM controller can be specified in the 'stm_commands.json' file.

_Example of `stm_commands.json` for the RHK PanScanFreedom via the R9_

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

## Contributing

We welcome contributions to pyxm! If you find a bug, have an enhancement idea, or want to add new features, please follow these steps:

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
