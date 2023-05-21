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
  "%tshark_path%" -r "%%~fI" >> "%output_file%"
)

echo Analysis complete. The output is saved in "%output_file%".

```