FROM chenzhuo/phpstudy

# 将应用程序文件复制到容器中
COPY ./src/app.php /var/www/html/app.php

# 定义容器启动时执行的命令
CMD ["php", "-S", "0.0.0.0:80", "-t", "/var/www/html"]
