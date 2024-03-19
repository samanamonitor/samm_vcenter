#!/bin/bash

set -x

if [ ! -d config ]; then
	mkdir -p config
	cp docs/conf.json config
fi

docker run -idt --name sammvcenter -p 80:80 -p 443:443 \
	-v $(pwd)/sammvcenter:/usr/local/sammvcenter \
	-v $(pwd)/httpd/httpd.conf:/usr/local/apache2/conf/httpd.conf \
	-v $(pwd)/httpd/samm:/usr/local/apache2/conf/samm \
	-v $(pwd)/config:/usr/local/sammvcenter/etc \
	sammvcenter
