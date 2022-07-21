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
    Latency    46.23ms   66.43ms 558.99ms   82.74%
    Req/Sec     3.30k     1.76k   19.07k    70.27%
  50158401 requests in 2.00m, 7.33GB read
Requests/sec: 417646.32
Transfer/sec:     62.53MB
</pre>

So based on the result, we can get the 30% performance improvement from OpenSSL.

|   Attempt    |   #JDK    | #OpenSSL  | improvement |
| :----------: | :-------: | :-------: | :---------: |
| Requests/sec | 313520.67 | 417646.32 |    1.33X    |
