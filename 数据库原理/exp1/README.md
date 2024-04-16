# 实验一

难点主要是 SQL Server 的安装，数据库管理工具进行数据库操作倒不是问题。

windows 下的安装过程跟着这篇文档走，很详细很详细：(Windows Server 安装SQL Server)[https://help.aliyun.com/document_detail/465370.html].

Linux 用户 参考这篇：[Microsoft 官方 Ubuntu 22.04 SQL Server 安装教程](https://learn.microsoft.com/zh-cn/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16&tabs=ubuntu2204)，可以直接使用同目录下的 `ubuntu-sqlserver-setup.sh` 安装 SQL Server。

安装成功后使用以下指令初始化 SQL Server：

- 会要求选择版本，推荐 Express 或者 Developer，我使用的是 Express；
- 初始化过程中要求设置密码，要求是包含大小写英文字母和阿拉伯数字的大于 8 位的字符串，我们这里就设置为 `SQLServer123`；

```shell
sudo /opt/mssql/bin/mssql-conf setup
```

安装配置完成后使用以下指令检查运行状态：

```shell
systemctl status mssql-server --no-pager
```

如果需要远程连接 SQL Server 还需要在服务器中开启 1443 端口。

> Linux 用户也不用我说吧，自己动手就好啦（笑

对于 Linux 用户，最推荐的方式是用 Docker 在本地起一个 SQL Server 服务，随用随开，不用就关，省心省事儿。本目录下有对应的 docker-compose.yml，怎么用就不必多说了。

最后，强烈建议不要使用实验要求的 SSMS 工具，老旧难用，绑外键时很麻烦，建议直接用 JetBrain 家的 DataGrip，省心省事儿高颜值。