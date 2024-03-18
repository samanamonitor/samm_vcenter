FROM httpd
RUN <<EOF
apt update && apt upgrade -y
apt install -y libapache2-mod-wsgi-py3 python3-flask python3-urllib3
EOF