FROM httpd:lastest
RUN <<EOF
apt udpate && apt upgrade -y
apt install -y libapache2-mod-wsgi-py3
EOF