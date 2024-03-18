#!/bin/bash

docker run --name sammvcenter -p 80:80 -v $(pwd)/sammvcenter:/usr/local/sammvcenter sammvcenter
