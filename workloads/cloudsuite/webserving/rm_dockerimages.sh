for tag in mysql memcached webserver client
do
	docker rmi sj-cloudsuite/web-serving:$tag
done
