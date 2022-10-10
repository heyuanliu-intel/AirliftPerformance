export LD_LIBRARY_PATH=/usr/local/ssl/lib/:$LD_LIBRARY_PATH
export OPENSSL_ENGINES=/usr/local/ssl/lib/engines-1.1/

openssl engine dynamic \
           -pre SO_PATH:/usr/local/ssl/lib/engines-1.1/qatengine.so \
           -pre LOAD 

openssl engine dynamic \
           -pre SO_PATH:qatengine \
           -pre LOAD 

cat /proc/`pgrep java`/maps | grep ssl
cat /proc/`pgrep java`/maps | grep qatengine