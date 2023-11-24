from scapy.all import *
import argparse
import datetime

# 定义回调函数，用于处理抓取到的数据包
def packet_handler(packet):
    global captured_packets
    global packet_counter

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

        # 将抓取到的IP数据包添加到列表中
        captured_packets.append(packet)
        packet_counter += 1

        # 每次抓取到10个IP数据包后停止抓包
        if packet_counter >= 10:
            return True  # 返回True停止抓包

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='IP数据包抓取和字段提取')
parser.add_argument('--host', help='只捕获与指定IP主机进行交互的流量')
parser.add_argument('--mac', help='只捕获与指定MAC地址的主机进行交互的流量')
parser.add_argument('--src', help='只捕获来源于指定IP的主机流量')
parser.add_argument('--port', help='只捕获指定端口的流量')
parser.add_argument('--exclude-port', help='捕获除了指定端口之外的流量')
parser.add_argument('--protocol', help='只捕获指定协议的流量')

# 解析命令行参数tf
args = parser.parse_args()

# 构建过滤器
filter_str = ""
if args.host:
    filter_str += "host " + args.host
if args.mac:
    filter_str += "ether host " + args.mac
if args.src:
    filter_str += "src host " + args.src
if args.port:
    filter_str += "port " + args.port
if args.exclude_port:
    filter_str += "!port " + args.exclude_port
if args.protocol:
    filter_str += args.protocol

# 创建一个空的列表，用于存储抓取到的IP数据包
captured_packets = []
packet_counter = 0

# 开始抓包
sniff(filter=filter_str, prn=packet_handler, stop_filter=lambda _: packet_counter >= 1)

# 获取程序开始运行时的时间戳
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 将抓取到的IP数据包写入文件
output_filename = f"./output/{timestamp}.pcap"
wrpcap(output_filename, captured_packets)
print("Captured packets saved to:", output_filename)
