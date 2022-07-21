#!/usr/bin/env sh

wrk -t128 -c2000 -d120s  https://localhost:9300/v1/service