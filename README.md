# AirliftPerformance

This project will evalute the performance improvement for TLS/SSL between the implementation of OpenJDK vs OpenSSL.

Below is the result for JDK implementation.

<pre>
./run_wrk.sh 
Running 2m test @ https://localhost:9300/v1/service
  128 threads and 2000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    38.86ms   51.92ms 433.64ms   80.04%
    Req/Sec     2.46k     1.32k   16.01k    72.29%
  37653716 requests in 2.00m, 5.51GB read
Requests/sec: 313520.67
Transfer/sec:     46.94MB
</pre>

Below is the result for OpenSSL implementation.

<pre>
Running 2m test @ https://localhost:9300/v1/service
  128 threads and 2000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    44.23ms   60.03ms 780.37ms   79.88%
    Req/Sec     3.40k     1.79k   22.39k    69.67%
  51789087 requests in 2.00m, 7.57GB read
Requests/sec: 431214.70
Transfer/sec:     64.56MB
</pre>

So based on the result, we can get the 38% performance improvement from OpenSSL.

|   Attempt    |   #JDK    | #OpenSSL  | improvement |
| :----------: | :-------: | :-------: | :---------: |
| Requests/sec | 313520.67 | 431214.70 |    1.38X    |
