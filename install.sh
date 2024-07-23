#!/bin/bash

set -x

SAMMVCETER_PATH=$1

if [ ! -d ${SAMMVCETER_PATH} ]; then
	mkdir -p ${SAMMVCETER_PATH}/
	mkdir -p ${SAMMVCETER_PATH}/htdocs
	cp docs/conf.json httpd/samm/sammvcenter.conf ${SAMMVCETER_PATH}
fi

docker run -idt --name sammvcenter -p 80:80 -p 443:443 \
	-v ${SAMMVCETER_PATH}/conf.json:/etc/sammvcenter/conf.json \
	-v ${SAMMVCETER_PATH}/sammvcenter.conf:/usr/local/apache2/conf/extra/sammvcenter.conf \
	-v ${SAMMVCETER_PATH}/htdocs:/usr/local/apache2/htdocs \
	sammvcenter
