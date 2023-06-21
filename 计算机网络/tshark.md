# tshark
```shell
@echo off
setlocal

set "tshark_path=C:\Program Files\Wireshark\tshark.exe"
set "output_file=output.txt"
set "directory=your_directory_path"

if not exist "%tshark_path%" (
  echo TShark is not found. Please specify the correct path to TShark.
  exit /b
)

if not exist "%directory%" (
  echo The specified directory does not exist.
  exit /b
)

for %%I in ("%directory%\*.*") do (
  echo Analyzing: %%~nxI
  "%tshark_path%" -r "%%~fI" -Y "your_filter_expression" >> "%output_file%"
)

echo Analysis complete. The output is saved in "%output_file%".

```
=====
```shell
@echo off
setlocal

set tshark_path="C:\Program Files\Wireshark\tshark.exe"  # 替换为tshark的安装路径
set pcap_folder="C:\path\to\pcap\folder"  # 替换为pcap包所在的文件夹路径
set output_file="C:\path\to\output.txt"  # 替换为输出文件的路径

for %%F in ("%pcap_folder%\*.pcap") do (
    echo Processing file: %%F
    %tshark_path% -r "%%F" -Y "your_filter_expression" -T fields -e frame.len -Y "frame.len>0" > nul && echo %%~nxF >> %output_file%
)

endlocal
```

=====
```python
import os
import pyshark

pcap_folder = "/path/to/pcap/folder"  # 替换为pcap包所在的文件夹路径
output_file = "/path/to/output.txt"  # 替换为输出文件的路径

# 获取pcap文件夹下的所有pcap文件路径
pcap_files = [os.path.join(pcap_folder, file) for file in os.listdir(pcap_folder) if file.endswith(".pcap")]

# 遍历每个pcap文件
for pcap_file in pcap_files:
    print("Processing file:", pcap_file)
    
    # 使用pyshark打开pcap文件
    cap = pyshark.FileCapture(pcap_file)
    
    # 判断包是否有数据，并将包的名称写入输出文件
    for packet in cap:
        if packet.length > 0:
            with open(output_file, "a") as f:
                f.write(os.path.basename(pcap_file) + "\n")
            break  # 如果找到有数据的包，可选择终止对该文件的遍历

    cap.close()
```