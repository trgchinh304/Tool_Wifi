# ! py
# Tool speedtest wifi
# Copyright by @Truongchinh304
# pip install speedtest-cli

import sys
import speedtest
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def test_wifi_speed():
    time_bd = datetime.now()
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  
    upload_speed = st.upload() / 1_000_000      
    ping = st.results.ping                     
    time_kt = datetime.now()
    time_delta = time_kt - time_bd  # Tổng thời gian đo
    print(f"Tốc độ tải xuống: {download_speed:.2f} Mbps")
    print(f"Tốc độ tải lên: {upload_speed:.2f} Mbps")
    print(f"Độ trễ (Ping): {ping} ms")
    print(f"Thời gian đo: {time_delta.seconds} giây {time_delta.microseconds // 1000} mili giây")

test_wifi_speed()
