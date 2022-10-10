#!/usr/bin/env sh
export LD_LIBRARY_PATH=/usr/local/ssl/lib/:$LD_LIBRARY_PATH
export OPENSSL_ENGINES=/usr/local/ssl/lib/engines-1.1/

if [ $provider == "qat" ]; then
    echo "run qat testing"
    mvn exec:java -Dexec.mainClass=example.Service -Dconfig=config_openssl.properties -Dorg.wildfly.openssl.engine=qatengine 
elif [ $provider == "openssl" ]; then
    echo "run openssl testing"
    mvn exec:java -Dexec.mainClass=example.Service -Dconfig=config_openssl.properties
else
    echo "run jdk testing"
    mvn exec:java -Dexec.mainClass=example.Service -Dconfig=config_jdk.properties
fi