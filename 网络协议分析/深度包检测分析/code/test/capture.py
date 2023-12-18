from scapy.all import sniff, wrpcap

# 回调函数，处理每个捕获到的数据包
def packet_callback(packet):
    # 将数据包写入pcap文件
    wrpcap('../package.pcap', packet, append=True)

# 捕获60秒内的lo设备上的所有数据包
sniff(iface='lo', timeout=60, prn=packet_callback)

print("数据包捕获完成并保存为package.pcap文件。")
