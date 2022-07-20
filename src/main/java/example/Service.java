package example;

import io.airlift.bootstrap.Bootstrap;
import io.airlift.event.client.EventModule;
import io.airlift.http.server.HttpServerModule;
import io.airlift.jaxrs.JaxrsModule;
import io.airlift.json.JsonModule;
import io.airlift.log.Level;
import io.airlift.log.Logging;
import io.airlift.log.LoggingConfiguration;
import io.airlift.node.NodeModule;
import org.wildfly.openssl.OpenSSLProvider;

import javax.net.ssl.SSLContext;

public class Service
{
    public static void main(String[] args) throws Exception
    {
        OpenSSLProvider.register();

        //String[] ciphers = OpenSSLContextSPI.getAvailableCipherSuites();
        SSLContext sslContext = SSLContext.getInstance("TLS", "openssl");
        SSLContext.setDefault(sslContext);

        Bootstrap app = new Bootstrap(new ServiceModule(),
                new NodeModule(),
                new HttpServerModule(),
                new EventModule(),
                new JsonModule(),
                new JaxrsModule());
        app.doNotInitializeLogging();

        Logging logging = Logging.initialize();
        logging.configure(new LoggingConfiguration());
        logging.setLevel("com.facebook.presto", Level.ERROR);
        logging.setLevel("org.eclipse.jetty.io.ssl", Level.ERROR);
        logging.setLevel("org.eclipse.jetty.io.thread", Level.ERROR);

        app.initialize();
    }

    private Service()
    {
    }
}
