FROM httpd
RUN <<EOF
apt update && apt upgrade -y
apt install -y libapache2-mod-wsgi-py3 python3-flask python3-urllib3
echo "Include conf/extra/sammvcenter.conf" >> /usr/local/apache2/conf/httpd.conf
EOF
COPY sammvcenter.py /usr/local/sammvcenter/sammvcenter.py
