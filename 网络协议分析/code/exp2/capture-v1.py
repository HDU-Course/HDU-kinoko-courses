from scapy.all import *

# 定义回调函数，用于处理抓取到的数据包
def packet_handler(packet):
    if IP in packet:
        ip_packet = packet[IP]
        timestamp = packet.time
        src_addr = ip_packet.src
        dst_addr = ip_packet.dst
        protocol = ip_packet.proto
        total_length = ip_packet.len
        ttl = ip_packet.ttl
        df = ip_packet.flags.DF
        mf = ip_packet.flags.MF
        offset = ip_packet.frag
        checksum = ip_packet.chksum

        # 打印字段值
        print("Timestamp:", timestamp)
        print("Source Address:", src_addr)
        print("Destination Address:", dst_addr)
        print("Protocol:", protocol)
        print("Total Length:", total_length)
        print("TTL:", ttl)
        print("DF:", df)
        print("MF:", mf)
        print("Offset:", offset)
        print("Checksum:", checksum)
        print("--------------------")

# 设置过滤器并开始抓包
# 只捕获与网络中某一IP主机进行交互的流量：host 1.1.1.1
sniff(filter="host 1.1.1.1", prn=packet_handler)

# 只捕获与网络中某以MAC地址的主机交互的流量：ether host 1c:4d:70:21:a3:a9
sniff(filter="ether host 1c:4d:70:21:a3:a9", prn=packet_handler)

# 只捕获来源于网路中某一个IP的主机流量：src host 1.1.1.1
sniff(filter="src host 1.1.1.1", prn=packet_handler)

# 捕获某端口的流量：port 80
sniff(filter="port 80", prn=packet_handler)

# 捕获除了某端口之外的流量：!port 80
sniff(filter="!port 80", prn=packet_handler)

# 捕获某协议的流量：icmp
sniff(filter="icmp", prn=packet_handler)