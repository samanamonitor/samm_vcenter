#!/bin/bash

set -x

SAMMVCETER_PATH=$1
HTTPPORT="${2:-80}"
HTTPSPORT="${3:-443}"

if [ -z ${SAMMVCETER_PATH} ]; then
	echo "Usage: $0 <path to sammvcenter>" >&2
	exit 1
fi

if [ ! -d ${SAMMVCETER_PATH} ]; then
	mkdir -p ${SAMMVCETER_PATH}/
	mkdir -p ${SAMMVCETER_PATH}/htdocs
	cp docs/conf.json httpd/samm/sammvcenter.conf ${SAMMVCETER_PATH}
fi

docker run -idt --name sammvcenter -p ${HTTPPORT}:80 -p ${HTTPSPORT}:443 \
	-v ${SAMMVCETER_PATH}/conf.json:/etc/sammvcenter/conf.json \
	-v ${SAMMVCETER_PATH}/sammvcenter.conf:/usr/local/apache2/conf/extra/sammvcenter.conf \
	-v ${SAMMVCETER_PATH}/htdocs:/usr/local/apache2/htdocs \
	sammvcenter
