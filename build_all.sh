export HOME=/home/heyuan
cd $HOME/wildfly-openssl-natives
mvn clean install -DskipTests 
cd $HOME/wildfly-openssl
mvn clean install -DskipTests
cd $HOME/AirliftPerformance
./build.sh