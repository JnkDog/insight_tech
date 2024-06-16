# #!/bin/bash

# # 文件路径
# STATUS_FILE="/var/lib/logrotate/status"

# # 检查文件是否存在
# if [ ! -f "$STATUS_FILE" ]; then
#   echo "Error: $STATUS_FILE does not exist."
#   exit 1
# fi

# # 检查文件是否为 ASCII 文本类型
# FILE_TYPE=$(file -b "$STATUS_FILE")
# if [[ "$FILE_TYPE" == *"ASCII text"* ]]; then
#   echo "$STATUS_FILE is an ASCII text file and is normal."
#   exit 0
# else
#   echo "Error: $STATUS_FILE is not an ASCII text file."
#   exit 1
# fi