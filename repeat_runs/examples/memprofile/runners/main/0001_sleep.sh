#!/bin/bash

(time sleep 5) 2>&1 | tee $1/commlog
