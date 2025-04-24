import re
import os
import socket
from argparse import Namespace

import distro
import psutil
import platform
import subprocess
import argparse

from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from datetime import datetime
from rich.console import Console
from dataclasses import dataclass
from screeninfo import get_monitors


@dataclass
class XToSeconds:
    """Constants for time conversion to seconds"""
    DAY_TO_SECONDS = 86400
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60


class TorchFetch:
    """Fetch and display system information in a formatted output"""

    def __init__(self) -> None:
        """Initialize TorchFetch with system information"""
        self.parser = self.arg_parser()
        self.theme = self.parser.theme if self.parser.theme else "default"

        self.console = Console()

        # Fetch system information
        self.os_info = self.get_os()
        self.host = self.get_host()
        self.kernel = self.get_kernel()
        self.uptime = self.get_uptime()
        self.packages = self.get_packages()
        self.shell = self.get_shell()
        self.resolution = self.get_resolution()
        self.de = self.get_de()
        self.cpu = self.get_cpu()
        self.gpu = self.get_gpu()
        self.memory = self.get_ram()

        # Set theme colors
        self.label_color, self.value_color, self.logo_color, self.border_style = self.set_theme(self.theme)

        self.logo = """                                                      
                                         88           
  ,d                                     88           
  88                                     88           
MM88MMM ,adPPYba,  8b,dPPYba,  ,adPPYba, 88,dPPYba,   
  88   a8"     "8a 88P'   "Y8 a8"     "" 88P'    "8a  
  88   8b       d8 88         8b         88       88  
  88,  "8a,   ,a8" 88         "8a,   ,aa 88       88  
  "Y888 `"YbbdP"'  88          `"Ybbd8"' 88       88  
                                                      
                                                      """

    @staticmethod
    def arg_parser() -> Namespace:
        parser = argparse.ArgumentParser(description="TorchFetch - A system information fetching tool")
        parser.add_argument("--theme", choices=["default", "dark", "light", "monochrome"],
                            default="default", help="Color theme to use")

        return parser.parse_args()

    @staticmethod
    def set_theme(theme_name: str) -> tuple[str, str, str, str]:
        """Set color theme for output
        
        Args:
            theme_name: Name of theme to use
        """
        themes = {
            "default": {
                "label_color": "bold cyan",
                "value_color": "white",
                "logo_color": "bold purple",
                "border_style": "bold purple"
            },
            "dark": {
                "label_color": "bold blue",
                "value_color": "bright_white",
                "logo_color": "bold green",
                "border_style": "bold green"
            },
            "light": {
                "label_color": "bold magenta",
                "value_color": "bright_black",
                "logo_color": "bold red",
                "border_style": "bold red"
            },
            "monochrome": {
                "label_color": "bold",
                "value_color": "white",
                "logo_color": "bold",
                "border_style": "bold"
            }
        }

        theme = themes.get(theme_name, themes["default"])

        return theme["label_color"], theme["value_color"], theme["logo_color"], theme["border_style"]

    @staticmethod
    def get_uptime() -> str:
        """Get system uptime

        Returns:
            Formatted uptime string
        """
        boot_time = psutil.boot_time()
        now = datetime.now().timestamp()

        uptime_seconds = int(now - boot_time)
        days, remainder = divmod(uptime_seconds, XToSeconds.DAY_TO_SECONDS)
        hours, remainder = divmod(remainder, XToSeconds.HOUR_TO_SECONDS)
        minutes, seconds = divmod(remainder, XToSeconds.MINUTE_TO_SECONDS)

        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        return uptime_str if uptime_str else "N/A"

    @staticmethod
    def get_shell() -> str:
        shell = os.environ.get('SHELL')
        return os.path.basename(shell) if shell else 'N/A'

    @staticmethod
    def get_de() -> str:
        de = os.environ.get('DESKTOP_SESSION') or os.environ.get('XDG_CURRENT_DESKTOP')
        return de if de else 'N/A'

    @staticmethod
    def get_resolution() -> str:
        monitors = get_monitors()
        resolutions = [f'{m.width}x{m.height}' for m in monitors]
        return ','.join(resolutions) if resolutions else "N/A"

    @staticmethod
    def get_packages() -> str:
        try:
            result = subprocess.run(['dpkg', '--get-selections'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                packages = len([line for line in result.stdout.split('\n') if line])
                return str(packages) + ' dpkg'
            return 'N/A'
        except subprocess.CalledProcessError as _:
            return 'N/A'
        except TimeoutError as _:
            return 'N/A'

    @staticmethod
    def get_os() -> str:
        return distro.name(pretty=True)

    @staticmethod
    def get_cpu() -> str:
        cpu = platform.processor()
        return cpu if cpu else 'N/A'

    @staticmethod
    def get_ram() -> str:
        return f'{round(psutil.virtual_memory().total / (1024 ** 2))}MB '

    @staticmethod
    def get_gpu() -> str:
        result = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        gpu_lines = re.findall(r'(VGA compatible controller|3D controller): (.+)', result.stdout, re.IGNORECASE)
        gpu_names = [gpu[1] for gpu in gpu_lines]

        return ','.join(gpu_names) if gpu_names else 'N/A'

    @staticmethod
    def get_host() -> str:
        return socket.gethostname()

    @staticmethod
    def get_kernel() -> str:
        return platform.release()

    def create_table(self) -> Table:
        table = Table(show_header=False, box=None, padding=(0, 1))

        table.add_row(Text('', style=self.label_color))
        table.add_row(Text('OS:', style=self.label_color), Text(self.os_info, style=self.value_color))
        table.add_row(Text('Host:', style=self.label_color), Text(self.host, style=self.value_color))
        table.add_row(Text('Kernel:', style=self.label_color), Text(self.kernel, style=self.value_color))
        table.add_row(Text('Uptime:', style=self.label_color), Text(self.uptime, style=self.value_color))
        table.add_row(Text('Packages:', style=self.label_color), Text(self.packages, style=self.value_color))
        table.add_row(Text('Shell:', style=self.label_color), Text(self.shell, style=self.value_color))
        table.add_row(Text('Resolution:', style=self.label_color), Text(self.resolution, style=self.value_color))
        table.add_row(Text('DE/WM:', style=self.label_color), Text(self.de, style=self.value_color))
        table.add_row(Text('CPU:', style=self.label_color), Text(self.cpu, style=self.value_color))
        table.add_row(Text('GPU:', style=self.label_color), Text(self.gpu, style=self.value_color))
        table.add_row(Text('RAM:', style=self.label_color), Text(self.memory, style=self.value_color))

        return table

    def print_console(self) -> None:
        table = self.create_table()

        logo_text = Text(self.logo, style=self.logo_color)
        logo_panel = Panel.fit(logo_text, border_style=self.border_style, padding=(0, 2))

        layout = Table.grid(expand=True)
        layout.add_column(justify='left', ratio=3)
        layout.add_column(justify='left', ratio=4)
        layout.add_row(logo_panel, table)

        self.console.print(Align.left(layout))


if __name__ == '__main__':
    my_fetch = TorchFetch()
    my_fetch.print_console()
