# 初始镜像
FROM python:3.7.5

# 更新并安装依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 设定在容器中的工作目录
WORKDIR /usr/src/app

# 安装python依赖
COPY requirements.txt ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple virtualenv \
         && virtualenv -p python env \
         && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

	

# 复制当前项目到容器中
COPY . .

# 暴露的端口
EXPOSE 8000

# 执行启动脚本
# RUN chmod a+x ./bin/ && sh ./bin/start.sh

# 启动容器
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
