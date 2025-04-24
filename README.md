# 🔥 TorchFetch

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.*](https://img.shields.io/badge/Python-3.*-blueviolet.svg)](https://www.python.org/downloads/)
[![Maintenance: Active](https://img.shields.io/badge/Maintenance-Active-success.svg)](https://github.com/cihaneray/TorchFetch)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20Windows%20%7C%20macOS-orange.svg)]()

A lightweight, customizable system information fetching tool that displays your system details in a beautiful, formatted output with a torch-inspired logo.

```                                                   
                                         88         
  ,d                                     88         
  88                                     88         
MM88MMM ,adPPYba,  8b,dPPYba,  ,adPPYba, 88,dPPYba, 
  88   a8"     "8a 88P'   "Y8 a8"     "" 88P'    "8a
  88   8b       d8 88         8b         88       88
  88,  "8a,   ,a8" 88         "8a,   ,aa 88       88
  "Y888 `"YbbdP"'  88          `"Ybbd8"' 88       88
```

## Features

- 🖥️ Displays comprehensive system information
- 🎨 Multiple color themes
- 🔍 Hardware detection (CPU, GPU, RAM)
- 🛠️ Software environment details
- 🖼️ Resolution detection
- ⏱️ System uptime display

## Requirements

TorchFetch depends on the following Python packages:
- rich
- psutil
- distro
- screeninfo
- platform (standard library)
- socket (standard library)
- subprocess (standard library)
- argparse (standard library)
- re (standard library)
- os (standard library)
- datetime (standard library)

## Installation

```bash
# Clone the repository
git clone [https://github.com/cihaneray/torchfetch.git](https://github.com/cihaneray/TorchFetch.git)
cd TorchFetch

# Install dependencies
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python torchfetch.py
```

With theme selection:
```bash
python torchfetch.py --theme dark
```

### Available Themes

TorchFetch offers four visual themes:
- `default` - Cyan labels with purple logo
- `dark` - Blue labels with green logo
- `light` - Magenta labels with red logo
- `monochrome` - Simplified black and white theme

## Information Displayed

TorchFetch displays the following system information:
- Operating System
- Hostname
- Kernel version
- System uptime
- Installed packages (dpkg)
- Current shell
- Screen resolution
- Desktop environment
- CPU information
- GPU details
- RAM size

## Customization

You can modify the torch logo or add additional system information by editing the source code. The logo is defined in the `logo` variable in the `TorchFetch` class.

## How It Works

TorchFetch uses various system libraries and commands to gather system information:
- `distro` for OS detection
- `psutil` for memory information and uptime
- `platform` for CPU and kernel details
- `socket` for hostname
- `subprocess` for package counting and GPU detection
- `screeninfo` for display resolution detection

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- The [Rich](https://github.com/Textualize/rich) library for beautiful terminal formatting
- Inspired by other system fetch tools like Neofetch and Screenfetch
