FROM python:3.9

# 指定 Image 中的工作目錄
WORKDIR /code

# 將 Dockerfile 所在目錄下的所有檔案複製到 Image 的工作目錄 /code 底下
ADD . /code

RUN pip install pymysql==1.0.2
RUN pip install urllib3==1.26.6
RUN pip install beautifulsoup4==4.9.3
RUN pip install bs4==0.0.1
RUN pip install lxml==4.6.3

CMD ["make", "run"]