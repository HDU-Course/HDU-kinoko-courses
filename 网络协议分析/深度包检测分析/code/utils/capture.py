from scapy.all import sniff, wrpcap

def packet_callback(packet):
    wrpcap('./package.pcap', packet, append=True)

print("[事件]：开始捕获数据包")

sniff(iface='lo', timeout=10, prn=packet_callback)

print("[事件]：数据包捕获完成并保存为package.pcap")
