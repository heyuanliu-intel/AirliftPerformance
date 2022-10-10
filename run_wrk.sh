#!/usr/bin/env sh

if [ "${alive}" == "false" ]; then
    echo "run short connection testing"
    wrk -t128 -c2000 -d120s -H "Connection: Close" https://localhost:9300/v1/service
else
    echo "run long connection testing"
    wrk -t128 -c2000 -d120s  https://localhost:9300/v1/service
fi

