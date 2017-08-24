for tag in mysql memcached webserver client
do
	docker rmi lb-cloudsuite/web-serving:$tag
done
