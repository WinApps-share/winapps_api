# 使用官方的 Python 映像作为基础映像
FROM python:3.8-slim

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录中的内容复制到容器的 /app 中
COPY . /app

# 安装应用程序所需的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器内部的 80 端口
EXPOSE 5000

# 定义启动容器时运行的命令
CMD ["python", "app.py"]
