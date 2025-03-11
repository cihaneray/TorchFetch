import re
import os
import socket
import distro
import psutil
import platform
import subprocess

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
    DAY_TO_SECONDS = 86400
    HOUR_TO_SECONDS = 3600
    MINUTE_TO_SECONDS = 60


class TorchFetch:
    def __init__(self) -> None:
        self.console = Console()

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

        self.label_color = 'bold cyan'
        self.value_color = 'white'
        self.bold_purple = 'bold purple'

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
    def get_uptime() -> str:
        boot_time = psutil.boot_time()
        now = datetime.now().timestamp()

        uptime_seconds = int(now - boot_time)
        days, remainder = divmod(uptime_seconds, XToSeconds.DAY_TO_SECONDS)
        hours, remainder = divmod(remainder, XToSeconds.HOUR_TO_SECONDS)
        minutes, seconds = divmod(remainder, XToSeconds.MINUTE_TO_SECONDS)

        uptime_str = f" {days}d {hours}h {minutes}m {seconds}s"
        return uptime_str

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
        try:
            monitors = get_monitors()
            resolutions = [f'{m.width}x{m.height}' for m in monitors]
            return ','.join(resolutions)
        except Exception:
            return 'N/A'

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
        per_ram = f'%{100 - psutil.virtual_memory().percent} used '
        total_ram = f'of {round(psutil.virtual_memory().total / (1024 ** 2))}MB '
        return per_ram + total_ram

    @staticmethod
    def get_gpu() -> str:
        try:
            result = subprocess.run(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            gpu_lines = re.findall(r'(VGA compatible controller|3D controller): (.+)', result.stdout, re.IGNORECASE)
            gpu_names = [gpu[1] for gpu in gpu_lines]

            return ','.join(gpu_names) if gpu_names else 'N/A'
        except Exception:
            return 'N/A'

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

        logo_text = Text(self.logo, style=self.bold_purple)
        logo_panel = Panel.fit(logo_text, border_style=self.bold_purple, padding=(0, 2))

        layout = Table.grid(expand=True)
        layout.add_column(justify='left', ratio=3)
        layout.add_column(justify='left', ratio=4)
        layout.add_row(logo_panel, table)

        self.console.print(Align.left(layout))


if __name__ == '__main__':
    my_fetch = TorchFetch()
    my_fetch.print_console()
