#!/bin/bash

if [ "$1" == "force" ]; then
	docker build -t sammvcenter:latest --no-cache .
else
	docker build -t sammvcenter:latest .
fi	

