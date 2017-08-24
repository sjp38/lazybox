#!/bin/bash

docker network create caching_network

# We set -n as 1024 as a survey[1] about Facebook memcached usage says so.
#
# [1] Atikoglu, Berk, et al. "Workload analysis of a large-scale key-value
#     store." ACM SIGMETRICS Performance Evaluation Review. Vol. 40. No. 1.
#     ACM, 2012.
docker run --name dc-server --net caching_network -d lb-cloudsuite/data-caching:server -t 4 -m 10240 -n 1024
