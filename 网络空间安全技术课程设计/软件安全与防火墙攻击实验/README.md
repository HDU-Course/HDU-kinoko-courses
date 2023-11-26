# 软件安全与防火墙攻击实验

## 搭建主机防火墙
在 Docker 容器中完成，在`firewall-deploy`目录下有需要的环境：

```shell
# 创建镜像及容器
sudo docker-compose up -d

# 进入容器交互式终端
sudo docker-compose exec ubuntu bash

# 加载防火墙规则
iptables-restore < /etc/iptables.rules

# 查看 iptables 链和对应规则
iptables -L -n -v

# 关闭并删除容器
sudo docker-compose down
```

## ”永恒之蓝“病毒感染复现

参考：[ms17-010 (永恒之蓝)漏洞复现及利用+Wireshark抓包分析](https://blog.csdn.net/qq_41210745/article/details/103343034)