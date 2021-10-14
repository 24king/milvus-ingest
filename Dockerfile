FROM docker.mirrors.iflytek.com:5000/iflytek/python3:3.8.6
# FROM centos:7.6.1810
# MAINTAINER limix coollimix@gmail.com
# RUN yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel gcc-c++ wget
# RUN wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tgz
# RUN tar -zxvf Python-3.8.6.tgz
# RUN cd Python-3.8.6
# WORKDIR /Python-3.8.6
# RUN yum install -y centos-release-scl
# RUN yum install -y devtoolset-8-gcc*
# RUN mv /usr/bin/gcc /usr/bin/gcc-4.8.5
# RUN ln -s /opt/rh/devtoolset-8/root/bin/gcc /usr/bin/gcc
# RUN mv /usr/bin/g++ /usr/bin/g++-4.8.5
# RUN ln -s /opt/rh/devtoolset-8/root/bin/g++ /usr/bin/g++
# RUN scl enable devtoolset-8 bash
# #RUN echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib" >> /etc/profile
#RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
#RUN ./configure --with-ssl --prefix=/usr/local/python38 --enable-optimizations --enable-shared 
#RUN make & make install
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/lib:/usr/local/python38/lib
ENV PATH $PATH:/usr/local/python38/bin
ADD ./ingest-kafka.py /opt/milvus-ingest/
ADD ./requirements.txt /opt/milvus-ingest/
WORKDIR /opt/milvus-ingest
RUN pip3 install -i https://pypi.douban.com/simple -r requirements.txt
CMD ["python3", "ingest-kafka.py"]
