import os
import time
import requests
from datetime import datetime

# 配置部分
PROBE_FILE_PATH = "/tmp/probe.cfg"
MX_PROCESS_NAME = "mx"
ETCD_API_URL = "http://example.com/get_etcd_address"  # 替换为实际的 API URL

def get_etcd_address():
    """
    调用接口获取 etcd 地址
    """
    try:
        response = requests.get(ETCD_API_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching etcd address: {e}")
        return None

def get_mx_process_restart_time():
    """
    获取 mx 进程的重启时间
    """
    try:
        result = os.popen(f"ps -eo pid,etime,cmd | grep {MX_PROCESS_NAME} | grep -v grep").read().strip()
        if result:
            # 假设 etime 格式为 "hh:mm:ss" 或 "dd-hh:mm:ss"
            etime = result.split()[1]
            time_parts = etime.split("-")
            if len(time_parts) == 2:
                days = int(time_parts[0])
                time_part = time_parts[1]
            else:
                days = 0
                time_part = time_parts[0]
            hours, minutes, seconds = map(int, time_part.split(":"))
            restart_time = datetime.now() - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            return restart_time
    except Exception as e:
        print(f"Error retrieving mx process restart time: {e}")
        return None

def check_and_update_probe_file():
    """
    检查 probe.cfg 文件，如果需要则更新 etcd 地址
    """
    update_needed = False
    
    if not os.path.exists(PROBE_FILE_PATH):
        print("probe.cfg file does not exist, will fetch etcd address.")
        update_needed = True
    else:
        file_mtime = os.path.getmtime(PROBE_FILE_PATH)
        file_mtime_datetime = datetime.fromtimestamp(file_mtime)

        mx_restart_time = get_mx_process_restart_time()
        if mx_restart_time and file_mtime_datetime < mx_restart_time:
            print("probe.cfg file was modified before mx restart, will fetch etcd address.")
            update_needed = True

    if update_needed:
        etcd_address = get_etcd_address()
        if etcd_address:
            try:
                with open(PROBE_FILE_PATH, "w") as f:
                    f.write(etcd_address)
                print(f"Etcd address '{etcd_address}' written to {PROBE_FILE_PATH}")
            except IOError as e:
                print(f"Error writing to {PROBE_FILE_PATH}: {e}")

if __name__ == "__main__":
    check_and_update_probe_file()