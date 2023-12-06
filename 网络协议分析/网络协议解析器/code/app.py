from flask import Flask, render_template, jsonify, request
from scapy.all import *

app = Flask(__name__)

"""
函数
"""
# 获取本地所有网络设备
def get_devices():
    devices = get_if_list()
    return devices

# 解析HTTP协议数据包
def parse_http(packet):
    if packet.haslayer('TCP') and packet.haslayer('Raw'):
        data = packet['Raw'].load.decode('utf-8', errors='ignore')
        return f"HTTP 数据: {data}"
    return "不包含HTTP协议数据"

# 解析TCP协议数据包
def parse_tcp(packet):
    if packet.haslayer('TCP'):
        src_port = packet['TCP'].sport
        dst_port = packet['TCP'].dport
        seq_num = packet['TCP'].seq
        ack_num = packet['TCP'].ack
        flags = packet['TCP'].flags
        window_size = packet['TCP'].window
        return f"TCP 源端口: {src_port}\n" \
               f"TCP 目标端口: {dst_port}\n" \
               f"TCP 序列号: {seq_num}\n" \
               f"TCP 确认号: {ack_num}\n" \
               f"TCP 标志位: {flags}\n" \
               f"TCP 窗口大小: {window_size}"
    return "不包含TCP协议数据"

# 解析UDP协议数据包
def parse_udp(packet):
    if packet.haslayer('UDP'):
        src_port = packet['UDP'].sport
        dst_port = packet['UDP'].dport
        length = packet['UDP'].len
        return f"UDP 源端口: {src_port}\n" \
               f"UDP 目标端口: {dst_port}\n" \
               f"UDP 长度: {length}"
    return "不包含UDP协议数据"

# 解析IP协议数据包
def parse_ip(packet):
    if packet.haslayer('IP'):
        timestamp = packet.time
        src_ip = packet['IP'].src
        dst_ip = packet['IP'].dst
        protocol = packet['IP'].proto
        total_length = packet['IP'].len
        ttl = packet['IP'].ttl
        df = packet['IP'].flags.DF
        mf = packet['IP'].flags.MF
        offset = packet['IP'].frag
        checksum = packet['IP'].chksum

        return f"时间戳: {timestamp}\n" \
               f"源 IP 地址: {src_ip}\n" \
               f"目标 IP 地址: {dst_ip}\n" \
               f"协议: {protocol}\n" \
               f"总长度: {total_length}\n" \
               f"TTL: {ttl}\n" \
               f"DF: {df}\n" \
               f"MF: {mf}\n" \
               f"偏移量: {offset}\n" \
               f"校验码: {checksum}"
    return "不包含IP协议数据"

# 解析Ethernet协议数据包
def parse_ethernet(packet):
    if packet.haslayer('Ether'):
        src_mac = packet['Ether'].src
        dst_mac = packet['Ether'].dst
        return f"源 MAC 地址: {src_mac}\n目标 MAC 地址: {dst_mac}"
    return "不包含Ethernet协议数据"

# 抓取数据包并解析
def capture_and_parse(device, packet_filter):
    print(f"抓取数据包: {device}, 过滤器: {packet_filter}")
    packets = sniff(iface=device, filter=packet_filter, count=1)
    result = ""
    for packet in packets:
        result += "HTTP：" + "\n" + parse_http(packet) + "\n"
        result += "TCP：" + "\n" + parse_tcp(packet) + "\n"
        result += "UDP：" + "\n" + parse_udp(packet) + "\n"
        result += "IP：" + "\n" + parse_ip(packet) + "\n"
        result += "Ethernet：" + "\n" + parse_ethernet(packet) + "\n"
    return result


"""
接口
"""
# ping测试接口
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'data': 'pong'})

@app.route('/devices', methods=['GET'])
def get_local_devices():
    devices = get_devices()
    return jsonify({'devices': devices})

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    device = data.get('device')
    packet_filter = data.get('filter')
    result = capture_and_parse(device, packet_filter)
    return result


"""
路由
"""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture/<device>', methods=['GET'])
def capture_page(device):
    return render_template('capture.html', device=device)


if __name__ == '__main__':
    app.run(port=5000, debug=True)