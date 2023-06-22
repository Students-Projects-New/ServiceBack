FROM ubuntu:20.04

COPY . /home/app


RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa

# RUN pip3 install --upgrade pip 

RUN apt-get install -y python3.9 \
&& apt install -y python3-pip

# RUN pip3 install -r requirements.txt
RUN apt install memcached -y
RUN apt install libmemcached-tools -y
RUN apt-get install python3-pymemcache libcache-memcached-libmemcached-perl -y
#RUN systemctl start memcached

RUN pip install -r /home/app/requirements.txt

# CMD ["gunicorn", "--bind", "0.0.0.0:8001", "sp_service_academic.wsgi", "-t", "600"]
# CMD ["python3.8","manage.py","runserver","0.0.0.0:8001"]
