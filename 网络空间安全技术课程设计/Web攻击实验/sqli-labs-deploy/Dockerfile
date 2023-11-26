FROM php:7.4-apache

# 添加apt-get换源指令
RUN sed -i 's/http:\/\/deb.debian.org\/debian\//http:\/\/mirrors.163.com\/debian\//g' /etc/apt/sources.list \
    && sed -i 's/http:\/\/security.debian.org\/debian-security\//http:\/\/mirrors.163.com\/debian-security\//g' /etc/apt/sources.list

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    telnet \
    inetutils-ping \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装sqli-labs
RUN git clone https://github.com/Audi-1/sqli-labs.git /var/www/html/sqli-labs

# 设置Apache的DocumentRoot
RUN sed -i 's/DocumentRoot \/var\/www\/html/DocumentRoot \/var\/www\/html\/sqli-labs/' /etc/apache2/sites-available/000-default.conf

# 启用Apache的rewrite模块
RUN a2enmod rewrite

# 设置容器的工作目录
WORKDIR /var/www/html/sqli-labs

# 暴露容器的端口
EXPOSE 80

# 启动Apache服务器
CMD ["apache2-foreground"]