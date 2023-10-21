# Use the Ubuntu 20.04 base image
FROM ubuntu:20.04

# Copy the custom source.list to the container
COPY sourcelist.txt /etc/apt/sources.list
# 修改时区
ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive
RUN apt update \
    && apt install -y tzdata \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# Update the package lists and install necessary dependencies
# RUN apt-get update && apt-get install software-properties-common -y && add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    wget \
    curl \
    unzip \
    git \
    android-tools-adb \
    tesseract-ocr \
    usbutils \
    python3-pip

# Install Google Chrome
# RUN wget -q  https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_110.0.5481.96-1_amd64.deb && apt-get install ./google-chrome-stable_110.0.5481.77-1_amd64.deb -y &&  apt-mark hold google-chrome-stable # 禁止更新
RUN wget -q  https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_110.0.5481.77-1_amd64.deb && apt-get install ./google-chrome-stable_110.0.5481.77-1_amd64.deb -y &&  apt-mark hold google-chrome-stable # 禁止更新
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip
RUN cd /tmp && unzip chromedriver.zip && mv chromedriver /usr/bin && chmod +x /usr/bin/chromedriver
# 下载最新的pip3
# RUN apt-get install python3.10-distutils
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
# 关联python3 到python3.10
#RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
#&& update-alternatives --install /usr/local/lib/python3.10/dist-packages/pip pip3 /usr/local/lib/python3.10/dist-packages/pip 1


# 使docker容器被手机信任
COPY adbkey /root/.android/adbkey
# Set the working directory
WORKDIR /app

# Copy your project files to the container
#COPY ["requirements.txt","./AppUIAutomator2Navigation","./context_sensitive_privacy_data_location","./Privacy-compliance-detection-2.1","run.py","get_urls.py","config.ini","/app/"]
COPY ["requirements_docker.txt","model","/app/"]
RUN pip3 install -r /app/requirements_docker.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && pip3 install --upgrade requests urllib3 chardet -i https://pypi.tuna.tsinghua.edu.cn/simple && pip3 install hanlp[full] -U -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ["requirements_yolov5.txt","/app/"]
RUN pip3 install -r /app/requirements_yolov5.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 下面这条语句配合.dockerignore使用，可以把dockerignore中的所有以！开头的文件/文件夹复制到指定位置，并且保持原有结构
COPY . /app
CMD ["/bin/bash"]