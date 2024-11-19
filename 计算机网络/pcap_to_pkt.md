## 代码
主要用来pcap文件转换为pkt
```shell
tshark -r input.pcap -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags > packets.txt
```


```pkt
0.000 socket(...);
0.001 bind(...);
0.002 connect(...);

+0.010 > IP 192.168.1.2.5000 > 192.168.1.1.80: Flags [S], seq 0, win 65535
+0.020 < IP 192.168.1.1.80 > 192.168.1.2.5000: Flags [S.], seq 0, ack 1, win 65535

```

```python
import csv

def convert_to_packetdrill(input_file, output_file):
    with open(input_file, 'r') as f, open(output_file, 'w') as out:
        reader = csv.reader(f, delimiter='\t')
        time_offset = 0
        for row in reader:
            timestamp, src, dst, src_port, dst_port, flags = row
            time_offset += 0.01  # 模拟时间偏移
            out.write(f"+{time_offset:.3f} > IP {src}.{src_port} > {dst}.{dst_port}: Flags [{flags}]\n")

convert_to_packetdrill('packets.txt', 'output.pkt')
```