## 一些常用脚本
```shell
#!/bin/bash

# 设置文件夹路径
folder_path="/path/to/your/pcap/files"

# 设置日志文件路径
log_file="filtered_pcap.log"

# 遍历文件夹中的pcap文件
for file in "$folder_path"/*.pcap; do
    # 使用tcpdump获取报文时间戳并计算间隔
    prev_timestamp=0
    while read -r line; do
        timestamp=$(echo "$line" | awk '{print $1}')
        if [ "$prev_timestamp" != 0 ]; then
            # 将时间戳转换为Unix时间戳
            current_unix=$(date -d "$timestamp" +"%s")
            prev_unix=$(date -d "$prev_timestamp" +"%s")
            # 计算时间间隔
            interval=$((current_unix - prev_unix))
            # 如果间隔大于15分钟，则将文件名写入日志文件并跳出循环
            if [ "$interval" -gt "900" ]; then
                echo "$file" >> "$log_file"
                break
            fi
        fi
        prev_timestamp=$timestamp
    done < <(tcpdump -r "$file" -ttt 2>/dev/null | awk '{print $1}')
done

echo "Filtered pcap files written to $log_file"
```

测试jio本2
```shell
#!/bin/bash

# 设置文件夹路径
folder_path="/path/to/your/pcap/files"

# 设置日志文件路径
log_file="filtered_pcap.log"

# 遍历文件夹中的pcap文件
for file in "$folder_path"/*.pcap; do
    # 使用tcpdump -r -ttt获取报文时间戳，然后使用grep和awk筛选出间隔大于15分钟的报文
    if tcpdump -r "$file" -ttt 2>/dev/null | grep -q -E '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\1' -A 1 | awk -v file="$file" 'NR==1{start=$1}NR==3{end=$1; interval=strftime("%s", end) - strftime("%s", start); if(interval > 900) {print file; exit}}'; then
        echo "$file" >> "$log_file"
    fi
done

echo "Filtered pcap files written to $log_file"
```