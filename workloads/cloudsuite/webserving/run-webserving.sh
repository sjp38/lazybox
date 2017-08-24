#!/bin/bash

docker run --net=host --name=faban_client lb-cloudsuite/web-serving:client 127.0.0.1 $1
