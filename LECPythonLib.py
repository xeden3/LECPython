import os
import subprocess
import sys
import platform
import urllib.request
import tempfile
import shutil
from typing import Dict, Any


class DotNetInstaller:
    RUNTIME_VERSION = "8"

    @staticmethod
    def check_runtime() -> bool:
        """
        Check if the specified version of .NET runtime is installed.
        """
        try:
            result = subprocess.run(['dotnet', '--list-runtimes'], capture_output=True, text=True, check=True)
            runtime_str = f' {DotNetInstaller.RUNTIME_VERSION}'
            installed = runtime_str in result.stdout
            # print(f"Checking if .NET runtime: {runtime_str} is installed: {installed}")
            return installed
        except subprocess.CalledProcessError as e:
            print(f"Executing dotnet command failed: {e}")
            return False
        except FileNotFoundError:
            print("dotnet command not found.")
            return False

    @staticmethod
    def install():
        """
        Install the .NET runtime.
        """
        if os.name == 'posix':
            print("Detected Linux environment.")
        elif os.name == 'nt':
            print("Detected Windows environment.")
        else:
            print("Unsupported operating system environment.")
            return

        distribution = platform.system().lower()
        try:
            if os.name == 'nt':  # Windows环境
                print("Detected Windows environment. Installing .NET 8 Runtime...")
                os.system('powershell -Command "& {Invoke-WebRequest -Uri https://dot.net/v1/dotnet-install.ps1 -OutFile dotnet-install.ps1; Set-ExecutionPolicy Bypass -Scope Process -Force; ./dotnet-install.ps1 -Channel 8.0 -Runtime dotnet}"')
            elif os.name == 'posix':
                if 'ubuntu' in distribution or 'debian' in distribution:
                    # Install .NET 8 on Ubuntu/Debian
                    print("Detected Ubuntu/Debian. Installing .NET 8 Runtime...")
                    os.system('sudo apt update')
                    os.system('sudo apt install -y wget')
                    os.system('wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb')
                    os.system('sudo dpkg -i packages-microsoft-prod.deb')
                    os.system('sudo apt update')
                    os.system('sudo apt install -y dotnet-runtime-8.0')
                
                elif 'centos' in distribution or 'rhel' in distribution or 'fedora' in distribution:
                    # Install .NET 8 on CentOS/RHEL/Fedora
                    print("Detected CentOS/RHEL/Fedora. Installing .NET 8 Runtime...")
                    os.system('sudo dnf install -y wget')
                    os.system('wget https://packages.microsoft.com/config/centos/8/packages-microsoft-prod.rpm -O packages-microsoft-prod.rpm')
                    os.system('sudo rpm -Uvh packages-microsoft-prod.rpm')
                    os.system('sudo dnf install -y dotnet-runtime-8.0')
                
                else:
                    # Other Linux distros
                    # if running on WSL, use apt to install dotnet-runtime-8.0
                    # else do not support install dotnet-runtime-8.0 by default
                    # output message to using manual installation 
                    with open("/proc/version", "r") as f:
                        version_info = f.read().lower()
                        if "microsoft" in version_info or "wsl" in version_info:
                            print("Detected Ubuntu/Debian. Installing .NET 8 Runtime...")
                            os.system('sudo apt update')
                            os.system('sudo apt install -y wget')
                            os.system('wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb')
                            os.system('sudo dpkg -i packages-microsoft-prod.deb')
                            os.system('sudo apt update')
                            os.system('sudo apt install -y dotnet-runtime-8.0')
                        elif "rpt-rpi" in version_info:
                            print("Detected Raspberry Pi environment. Installing .NET 8 Runtime...")
                            os.system('sudo apt update')
                            os.system('sudo apt install -y wget')
                            os.system('wget -O aspnetcore-runtime-8.0.8-linux-arm64.tar.gz https://download.visualstudio.microsoft.com/download/pr/f6fcf2c9-39ad-49c7-80b5-92306309e796/3cac9217f55528cb60c95702ba92d78b/aspnetcore-runtime-8.0.8-linux-arm64.tar.gz')
                            os.system('sudo mkdir -p /usr/share/dotnet')
                            os.system('sudo tar zxf aspnetcore-runtime-8.0.8-linux-arm64.tar.gz -C /usr/share/dotnet')
                            os.system('sudo ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet')
                        else:
                            raise RuntimeError("Automatic installation of .NET runtime is not supported. Please install .NET runtime manually.")
                    
            # Verify installation
            result = subprocess.run(['dotnet', '--list-runtimes'], stdout=subprocess.PIPE, text=True)
            if f' {DotNetInstaller.RUNTIME_VERSION}' in result.stdout:
                print("Installation successful! .NET 8 Runtime is installed.")
            else:
                print("Failed to verify .NET 8 Runtime installation. Check for errors above.")
        
        except Exception as e:
            print(f"An error occurred during installation: {e}")

class LECPython:
    def __init__(self):
        """
        Initialize the LECPython instance, check and install .NET runtime, load C# DLL.
        """
        if not DotNetInstaller.check_runtime():
            print(f".NET runtime {DotNetInstaller.RUNTIME_VERSION} not detected, installing...")
            try:
                DotNetInstaller.install()
            except RuntimeError as e:
                print(f"Unable to install .NET runtime: {e}")
                sys.exit(1)
            print(f".NET runtime {DotNetInstaller.RUNTIME_VERSION} installation completed.")

        try:
            from pythonnet import load
            load("coreclr")
            # print("Loaded coreclr successfully.")
        except Exception as e:
            # print(f"Loading coreclr failed: {e}")
            raise RuntimeError("Failed to load coreclr.") from e

        try:
            import clr
            dll_path = os.path.join(os.path.dirname(__file__), "LECPythonLib.dll")
            clr.AddReference(dll_path)
            # print(f"Successfully added reference: {dll_path}")
        except Exception as e:
            # print(f"Adding CLR reference failed: {e}")
            raise RuntimeError("Failed to add CLR reference.") from e

        try:
            from LECPythonLib import DeviceProfinetConnection, DeviceProfinetCommunication
            self.connection = DeviceProfinetConnection()
            self.communication = DeviceProfinetCommunication()
            # print("Successfully imported LECPythonLib namespace.")
        except Exception as e:
            print(f"Importing LECPythonLib namespace failed: {e}")
            raise RuntimeError("Failed to import LECPythonLib namespaces.") from e

    def __getattr__(self, method_name: str):
        """
        Dynamically handle method calls.
        """
        def method(*args, **kwargs) -> Dict[str, Any]:
            if hasattr(self.connection, method_name):
                try:
                    result = getattr(self.connection, method_name)(*args, **kwargs)
                    return {
                        "ErrorCode": result.ErrorCode,
                        "IsSuccess": result.IsSuccess,
                        "Message": result.Message,
                        "Content": result.Content
                    }
                except Exception as e:
                    print(f"Calling method {method_name} failed: {e}")
                    raise
            else:
                error_msg = f"'{self.connection.__class__.__name__}' object has no method '{method_name}'"
                print(error_msg)
                raise AttributeError(error_msg)
        return method

    def ReadNodeValues(self, plc: str, address: str, data_type: str, length: int) -> Dict[str, Any]:
        """
        Read node values from PLC.
        """
        try:
            result = self.communication.ReadNodeValues(plc, address, data_type, length)
            content_array = [] if not result.IsSuccess else (result.Content if isinstance(result.Content, list) else list(result.Content))
            return {
                "ErrorCode": result.ErrorCode,
                "IsSuccess": result.IsSuccess,
                "Message": result.Message,
                "Content": content_array
            }
        except Exception as e:
            print(f"Failed to read node values: {e}")
            raise

    def WriteNodeValues(self, plc: str, address: str, data_type: str, value: Any) -> Dict[str, bool]:
        """
        Write node values to PLC.
        """
        try:
            success = self.communication.WriteNodeValues(plc, address, data_type, value)
            return {"IsSuccess": success}
        except Exception as e:
            print(f"Failed to write node values: {e}")
            raise

    def Test(self) -> Dict[str, bool]:
        """
        Perform test operation.
        """
        try:
            success = self.connection.Test()
            return {"IsSuccess": success}
        except Exception as e:
            print(f"Test connection failed: {e}")
            raise
