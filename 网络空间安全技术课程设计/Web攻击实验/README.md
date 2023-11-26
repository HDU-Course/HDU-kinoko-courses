## Web攻击实验
建议找队友一块做，工作量略大。

主要是写文档很烦，最好是有人喜欢写文档就专门写文档，然后懂技术的搭建环境，合理分工。

嫌麻烦可以去网上找打过对应靶场的教程copy直接截图，专注于写文档。

## 学习Web攻击
### SQL-ILabs 
搭建靶场可以使用该目录下`sqli-labs-deploy`目录中的 Dockerfile 和 docker-compose.yml。

```shell
sudo docker-compose up -d

sudo dockerps

sudo docker-compose down
```

参考：[SQL注入靶场sqli-labs 1-65关全部通关教程 ](https://www.cnblogs.com/-qing-/p/11610385.html)

### Apache Log4J2漏洞复现（选做）
参考：[vulhub](https://github.com/vulhub/vulhub/tree/master/log4j/CVE-2021-44228)