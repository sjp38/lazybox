#!/bin/bash

#docker run -dt --net=host --name=mysql_server cloudsuite/web-serving:db_server 127.0.0.1
#docker run -dt --net=host --name=memcache_server cloudsuite/web-serving:memcached_server
#docker run -dt --net=host --name=web_server cloudsuite/web-serving:web_server /etc/bootstrap.sh 127.0.0.1 127.0.0.1 80

docker run -dt --net=host --name=mysql_server sj-cloudsuite/web-serving:mysql 127.0.0.1
docker run -dt --net=host --name=memcache_server sj-cloudsuite/web-serving:memcached
docker run -dt --net=host --name=web_server sj-cloudsuite/web-serving:webserver /etc/bootstrap.sh 127.0.0.1 127.0.0.1 80
