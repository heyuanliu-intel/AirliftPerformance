#!/usr/bin/env sh
export LD_LIBRARY_PATH=/usr/local/ssl/lib/:$LD_LIBRARY_PATH
export OPENSSL_ENGINES=/usr/local/ssl/lib/engines-1.1/

mvn exec:java -Dexec.mainClass=example.Service -Dconfig=config.properties -Dorg.wildfly.openssl.engine=qatengine