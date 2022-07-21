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
    Latency    39.70ms   53.82ms 304.35ms   79.91%
    Req/Sec     3.65k     1.98k   20.13k    69.97%
  55615058 requests in 2.00m, 8.13GB read
Requests/sec: 463086.91
Transfer/sec:     69.34MB
</pre>

So based on the result, we can get the 48% performance improvement from OpenSSL.

|   Attempt    |   #JDK    | #OpenSSL  | improvement |
| :----------: | :-------: | :-------: | :---------: |
| Requests/sec | 313520.67 | 463086.91 |    1.48X    |
