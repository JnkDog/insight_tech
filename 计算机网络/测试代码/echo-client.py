import requests
import logging
import time

logging.basicConfig(filename='error_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

target_url = 'http://124.70.69.142/api/v3/file/healthcheck.txt'
demo_url = '127.0.0.1:3300'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Host': 'honeycomb.wps.cn'
}

request_interval = 30
TMOUT = 5

def send_request(url):
    try:
        response = requests.get(url, timeout=TMOUT, headers=headers)
        response.raise_for_status()
        logging.info("ok")
    except requests.RequestException as e:
        logging.error("  is : {}", e)
    
if __name__ == '__main__':
    while True:
        send_request(target_url)
        time.sleep(request_interval)