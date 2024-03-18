#!/bin/bash

mkdir -p config
docker run --name sammvcenter -p 80:80 \
	-v $(pwd)/sammvcenter:/usr/local/sammvcenter \
	-v $(pwd)/config:/usr/local/httpd/sammvcenter \
	sammvcenter
