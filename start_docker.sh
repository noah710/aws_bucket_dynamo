#!/bin/bash
docker build -f Dockerfile -t cloudstorage_hw . \
	&& docker run -it -e keyid=${1} -e keysecret=${2} -v "$(pwd)"/scripts:/scripts -v "$(pwd)"/data:/data cloudstorage_hw bash
