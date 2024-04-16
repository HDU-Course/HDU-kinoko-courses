#!/bin/bash

# 停止脚本在遇到错误时继续执行
set -e

# 导入 Microsoft GPG 公钥
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

# 添加 SQL Server 仓库到系统源列表
curl -fsSL https://packages.microsoft.com/config/ubuntu/22.04/mssql-server-2022.list | sudo tee /etc/apt/sources.list.d/mssql-server-2022.list

# 更新本地包列表
sudo apt-get update

# 安装 SQL Server
sudo apt-get install -y mssql-server

# 提示
echo "SQL Server 安装完成"
