# LECPython

LECPython is a Python component developed in C# that enables seamless communication between Python and PLCs. It requires .NET 8 runtime support. When LECPython is called for the first time, the component automatically checks if .NET 8 is installed, and if not, it will perform an automatic online installation.

LECPython supports a wide range of PLCs available in the market, including those supporting the Modbus protocol, Mitsubishi, Siemens, Omron, Rockwell, Keyence PLC, Delta, Beckhoff, Panasonic, Inovance, Fuji, EverSensing, Schneider, and more. This component is standalone, requiring no additional third-party PLC controls for support.

# Introduction

LECPython provides a simple and efficient way to connect and communicate with various PLCs. Whether for industrial automation or other applications requiring PLC control, LECPython offers a reliable solution. Since LECPython is developed in C#, its read and write efficiency is faster than pure Python.

The operation process of LECPython is as follows: First, a connector is created through `DeviceProfinetConnection`, but it does not connect to the PLC at this time. During the first read and write operation to the PLC, the actual connection and communication with the PLC are performed through `DeviceProfinetCommunication`. The connector automatically completes the long connection and reconnection mechanism. As long as the `DeviceProfinetConnection` object is not cleared, the connector remains effective. Meanwhile, users can set the connector's `data_format` and `is_string_reverse_byte_word` to achieve high and low byte read settings for the PLC.

# Getting Started

## Installation

Ensure you have Python installed. You can install LECPython using pip:

```bash
pip install LECPython
```

LECPython automatically installs the required `pythonnet` dependency. However, if needed, you can manually install it using:

```bash
pip install pythonnet==3.0.4
```

## .NET 8 Installation

LECPython requires .NET 8 runtime support. When you call LECPython for the first time, the component will automatically check if .NET 8 is installed on your system. If not, LECPython will automatically install the .NET 8 runtime online.

### Automatic Installation Steps

1. When you run LECPython for the first time, the component will check if .NET 8 runtime is present on your system.
2. If .NET 8 runtime is not detected, LECPython will attempt to download and install .NET 8 online.
3. The installation process will vary depending on the operating system. If the automatic installation fails, LECPython will prompt you to manually install .NET 8.

### Manual Installation

If the automatic installation fails, you can manually install .NET 8 by following these steps:

- For Windows users:
  1. Visit the official .NET website: https://dotnet.microsoft.com/download/dotnet/8.0
  2. Download and run the installer for Windows.

- For Ubuntu users:
  ```bash
  wget https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-8.0.0-linux-x64-binaries
  tar -zxf dotnet-runtime-8.0.0-linux-x64.tar.gz -C $HOME/dotnet
  export PATH=$PATH:$HOME/dotnet
  ```

- For users of other Linux distributions, please refer to the installation guide on the official .NET website.

### Supported Systems

LECPython has been tested and confirmed to automatically complete the .NET 8 installation on the following systems:
- Ubuntu 20.04, 22.04
- Windows 11 WSL2 environment
- Windows 11 PowerShell environment
- Raspbian OS environment on Raspberry Pi

## Usage Example

Here's a basic example of how to use LECPython:

```python
from LECPython import LECPython

if __name__ == "__main__":
    lecp = LECPython()
    try:
        # Establish connection to Omron FINS PLC
        result = lecp.OmronFinsNetConnection("192.168.31.64", 9600, 13, 0, "CDAB", True, 2000)
        print("Omron FINS PLC Connection called successfully:", result["ErrorCode"])
        
        # Read 10 float values from address D100
        rtval = lecp.ReadNodeValues(result["Content"], "D100", "float", 10)
        print(f"The PLC read rtval is: {rtval}")
        
        # Write a float value to address D100
        rtval = lecp.WriteNodeValues(result["Content"], "D100", "float", [88.123, 726.1223])
        print(f"The PLC write rtval is: {rtval}")
        
        # Read 10 float values from address D100 again
        rtval = lecp.ReadNodeValues(result["Content"], "D100", "float", 10)
        print(f"The PLC read rtval is: {rtval}")

        # Close connection
        lecp.ConnectClose(result["Content"])
    except AttributeError as e:
        print(e)
```


# Features

- Supports multiple PLC protocols including Modbus, Mitsubishi, Siemens, Omron, Rockwell, and more.
- Easy to use API for connecting and communicating with PLCs.
- Standalone component with no need for additional third-party PLC controls.
- Built-in .NET 8 runtime automatic installation.

For more detailed API documentation, please visit: [LECPython API Documentation](http://www.lecpserver.com:3003/)

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

-----

# LECPython （中文）

LECPython 是一个用 C# 开发的 Python 组件，能够实现 Python 与 PLC 之间的无缝通信。它需要 .NET 8 运行时支持，当首次调用 LECPython 时，组件会自动检查是否安装了 .NET 8，如果没有，它将自动在线安装。

LECPython 支持市场上广泛的 PLC，包括支持 Modbus 协议的 PLC、三菱、西门子、欧姆龙、罗克韦尔、基恩士、台达、倍福、松下、汇川、富士、EverSensing、施耐德等。该组件是独立的，不需要额外的第三方 PLC 控件支持。

# 简介

LECPython 提供了一种简单而高效的方式来连接和通信各种 PLC。无论是工业自动化还是其他需要 PLC 控制的应用，LECPython 都能提供可靠的解决方案。由于 LECPython 是基于 C# 开发的，因此其运行读写效率会比纯 Python 快。

LECPython 的运行过程如下：首先通过 `DeviceProfinetConnection` 创建一个连接器，但此时并不会与 PLC 进行连接。在第一次读写 PLC 时，通过 `DeviceProfinetCommunication` 操作，对 PLC 进行实际的连接和通讯。连接器自动完成长连接和断线重连的机制，只要 `DeviceProfinetConnection` 对象不被清除，连接器就一直有效。同时，用户可以通过设置连接器的 `data_format` 和 `is_string_reverse_byte_word` 来实现 PLC 的高低位读取设定。




# 使用指南

## 安装

确保你已经安装了 Python。你可以使用 pip 安装 LECPython：

```bash
pip install LECPython
```

LECPython 会自动安装所需的 `pythonnet` 依赖项。如果需要，你也可以手动安装：

```bash
pip install pythonnet==3.0.4
```
## .NET 8 安装

LECPython 需要 .NET 8 运行时支持。当你第一次调用 LECPython 时，组件会自动检查系统中是否安装了 .NET 8。如果没有安装，LECPython 将会自动在线安装 .NET 8 运行时。

### 自动安装步骤

1. 当你第一次运行 LECPython 时，组件会检测系统中是否存在 .NET 8 运行时。
2. 如果没有检测到 .NET 8 运行时，LECPython 将会尝试在线下载并安装 .NET 8。
3. 安装过程会根据操作系统的不同而有所不同。如果自动安装失败，LECPython 会提示你手动安装 .NET 8。

### 手动安装

如果自动安装失败，你可以根据以下步骤手动安装 .NET 8：

- 对于 Windows 用户：
  1. 访问 .NET 官方网站：https://dotnet.microsoft.com/download/dotnet/8.0
  2. 下载并运行适用于 Windows 的安装程序。

- 对于 Ubuntu 用户：
  ```bash
  wget https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-8.0.0-linux-x64-binaries
  tar -zxf dotnet-runtime-8.0.0-linux-x64.tar.gz -C $HOME/dotnet
  export PATH=$PATH:$HOME/dotnet
  ```

- 对于其他 Linux 发行版用户，请参考 .NET 官方网站上的安装指南。

### 支持的系统

LECPython 已在以下系统上测试并确认可以自动完成 .NET 8 的安装：
- Ubuntu 20.04, 22.04
- Windows 11 WSL2 环境
- Windows 11 PowerShell 环境
- 树莓派的 Raspbian OS 环境

## 使用示例

以下是一个如何使用 LECPython 的基本示例：

```python
from LECPython import LECPython

if __name__ == "__main__":
    lecp = LECPython()
    try:
        # 开启连接器 欧姆龙 FINS PLC
        result = lecp.OmronFinsNetConnection("192.168.31.64", 9600, 13, 0, "CDAB", True, 2000)
        print("Omron FINS PLC Connection 调用成功:", result["ErrorCode"])
        
        # 从地址 D100 读取 10 个浮点值
        rtval = lecp.ReadNodeValues(result["Content"], "D100", "float", 10)
        print(f"读取的值是: {rtval}")
        
        # 向地址 D100 写入浮点值
        rtval = lecp.WriteNodeValues(result["Content"], "D100", "float", [88.123, 726.1223])
        print(f"写入的值是: {rtval}")
        
        # 再次从地址 D100 读取 10 个浮点值
        rtval = lecp.ReadNodeValues(result["Content"], "D100", "float", 10)
        print(f"读取的值是: {rtval}")

        # 关闭连接器
        lecp.ConnectClose(result["Content"])
    except AttributeError as e:
        print(e)
```

# 特点

- 支持多种 PLC 协议，包括 Modbus、三菱、西门子、欧姆龙、罗克韦尔等。
- 提供易于使用的 API，用于连接和通信 PLC。
- 独立组件，无需额外的第三方 PLC 控件。
- 自带 .NET 8 运行时自动安装。

需要了解更多的API信息，请查阅官方文档: [LECPython API Documentation](http://www.lecpserver.com:3003/)

# 许可证

此项目根据 MIT 许可证授权。详情请参阅 [LICENSE](LICENSE) 文件。
