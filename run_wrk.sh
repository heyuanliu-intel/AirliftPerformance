#!/usr/bin/env sh

wrk -t128 -c2000 -d600s  https://localhost:9300/v1/service