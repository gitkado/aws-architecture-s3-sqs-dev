FROM python:3.8.5-slim-buster

ENV APP_ROOT /opt/app
WORKDIR $APP_ROOT

COPY sh/container_startup.sh /run/container_startup.sh
COPY sh/wait-for-mysql.sh /run/wait-for-mysql.sh
COPY requirements.txt /opt/requirements.txt

RUN apt update && \
    apt install -y python-dev default-libmysqlclient-dev mariadb-client gcc apt-utils libpcre3-dev gnupg wget && \
    wget https://nginx.org/keys/nginx_signing.key && \
    apt-key add nginx_signing.key && \
    echo "deb http://nginx.org/packages/debian/ buster nginx" >> "/etc/apt/sources.list" && \
    echo "deb-src http://nginx.org/packages/debian/ buster nginx" >> "/etc/apt/sources.list" && \
    apt update && \
    apt install -y nginx && \
    rm -f /etc/nginx/sites-enabled/default && \
    apt clean && \
    apt autoclean && \
    mkdir /run/uwsgi && \
    chmod -R 777 /run

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /opt/requirements.txt && \
    rm -f /opt/requirements.txt

COPY nginx/app.conf /etc/nginx/conf.d/app.conf
COPY src $APP_ROOT

EXPOSE 80

ENTRYPOINT ["/run/wait-for-mysql.sh", "mysql"]

CMD ["/run/container_startup.sh"]