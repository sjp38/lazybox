#!/bin/bash

docker run --net=host --name=faban_client sj-cloudsuite/web-serving:client 127.0.0.1 $1
