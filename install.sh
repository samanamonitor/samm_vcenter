#!/bin/bash

set -x

mkdir -p config
docker run -idt --name sammvcenter -p 80:80 \
	-v $(pwd)/sammvcenter:/usr/local/sammvcenter \
	-v $(pwd)/httpd/httpd.conf:/usr/local/apache2/conf/httpd.conf \
	-v $(pwd)/httpd/sammvcenter.conf:/usr/local/apache2/conf/sammvcenter.conf \
	sammvcenter
