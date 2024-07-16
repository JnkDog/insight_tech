from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.vxlan import VXLAN

def extract_and_save_vxlan_inner_packets(input_pcap, output_pcap):
    packets = rdpcap(input_pcap)
    inner_packets = []

    for packet in packets:
        if VXLAN in packet:
            vxlan_packet = packet[VXLAN]
            inner_packet = vxlan_packet.payload
            inner_packets.append(inner_packet)

    wrpcap(output_pcap, inner_packets)
    print(f"Extracted and saved {len(inner_packets)} inner packets to {output_pcap}")

def main():
    input_pcap = 'vxlan-demo/vxlan.pcap'
    output_pcap = 'free-vxlan.pcap'
    extract_and_save_vxlan_inner_packets(input_pcap, output_pcap)

if __name__ == "__main__":
    main()
