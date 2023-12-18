# 网络协议分析
## 实验一：网络数据包分析
学习使用Wireshark工具即可。

## 实验二：抓取IP数据包
`capture-v3.py`可完成实验要求，即通过参数设置不同的过滤规则抓取IP数据包，并返回要求的数据。

需要`scapy`库环境，不需要修改源文件，在命令后面添加对应的参数即可实现制定的过滤规则。

> 仅支持单个参数，不支持同时使用两个及两个以上的参数。

使用案例：

```shell
sudo python capture_packets.py --host 1.1.1.1
sudo python capture_packets.py --mac 1c:4d:70:21:a3:a9
sudo python capture_packets.py --src 1.1.1.1
sudo python capture_packets.py --port 80
sudo python capture_packets.py --exclude-port 80
sudo python capture_packets.py --protocol icmp
```

## 实验三：简易网络协议解析器
给实验二做个壳，使用flask实现的简易网页版解析器。使用以下指令运行服务：
```shell
sudo python app.py
```

访问[http://localhost:5000](http://localhost:5000)，然后使用相应功能即可。

注意，仓库中该段代码实现的非常非常丑陋（存储数据包文件还有随机崩溃问题），但当作实验验收还是够了。建议仅作实验验收使用🙃。

## 实验四：深度包检测分析
