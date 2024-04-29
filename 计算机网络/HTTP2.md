# http2
1. 直观感受HTTP2和 HTTP1.1的区别
https://http2.akamai.com/demo

2. 如果配置的是http2的ngx，不走tls，那么需要加 --http2-prior-knowledge
```shell
curl offers the --http2 command line option to enable use of HTTP/2.

curl offers the --http2-prior-knowledge command line option to enable use of HTTP/2 without HTTP/1.1 Upgrade. (如果升级不支持的情况下)

3. https://imququ.com/post/http2-traffic-in-wireshark.html https 抓

4. nghttp 调试

## okhttp2的http2诡异的实现
1. 先用javaagent拿到pre master key. 先觉条件是有这个jar包，idea放在vm options下
-javaagent:extract-tls-secrets-4.0.0.jar=tls.log
2. 测试代码，okhttp版本 3.12.6
```java
/**
 <dependency>
            <groupId>com.squareup.okhttp3</groupId>
            <artifactId>okhttp</artifactId>
            <version>3.12.6</version>
        </dependency>
**/
public class Main {
    public static void main(String[] args) throws InterruptedException {
        // default 5min
        ConnectionPool pool = new ConnectionPool(2, 30, TimeUnit.SECONDS);
        OkHttpClient client = new OkHttpClient.Builder().connectionPool(pool).build();
        String urlTest1 = "xxx";
        String urlTest2 = "xxx";
        Request request1 = new Request.Builder().url(urlTest1).get().build();
        Request request2 = new Request.Builder().url(urlTest2).get().build();
        Request request3 = new Request.Builder().url("xxx").get().build();
        Call call1 = client.newCall(request1);
        Call call2 = client.newCall(request2);
        Call call3 = client.newCall(request3);
        call1.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.printf("t1请求失败,异常信息为: {%s}", e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                System.out.printf("t1请求成功: {%s}\n", response.code());
            }
        });
        call2.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.printf("t2请求失败,异常信息为: {%s}", e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                System.out.printf("t2请求成功: {%s}\n", response.code());
            }
        });

        call3.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.printf("t3请求失败,异常信息为: {%s}", e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                System.out.printf("t3请求成功: {%s}\n", response.code());
            }
        });
        System.out.println("ok ... ???");
    }
}
```
抓包发现他的实现是很奇怪的，具体操作是
====    

```java
public class Main {
//    private static final Logger logger = LoggerFactory.getLogger();
    public static final int CONNECTION_POOL_SIZE = 20;

    public static final int CONNECTION_ALIVE_TIMEOUT = 5;

    public static final String BASE_URL = "xxx";

    public static void main(String[] args) throws InterruptedException {
        // default 5min
        ConnectionPool pool = new ConnectionPool(CONNECTION_POOL_SIZE, CONNECTION_ALIVE_TIMEOUT, TimeUnit.MINUTES);
        OkHttpClient client = new OkHttpClient.Builder().connectionPool(pool).build();
        testSendRequestByTime(20, client);
        Thread.sleep(2000);
        String delayTwoSecondUrl = new StringBuilder(BASE_URL).append("test").append("/delay-2").toString();
        Request request = new Request.Builder().url(delayTwoSecondUrl).get().build();
        Call call = client.newCall(request);
        call.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.printf("delay请求失败,异常信息为: {%s}", e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                System.out.printf("delay请求成功: {%s}\n", response.code());
            }
        });
        System.out.println("what???");
    }

    public static void testSendRequestByTime(int times, OkHttpClient client) {
        for (int i = 0; i < times; i++) {
            String testUrl = new StringBuilder(BASE_URL).append("test").append(i).toString();
            Request request = new Request.Builder().url(testUrl).get().build();
            Call call = client.newCall(request);
            int idx = i;
            call.enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    System.out.printf("第{%d}次请求失败,异常信息为: {%s}", idx + 1, e.getMessage());
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    System.out.printf("第{%d}次请求成功: {%s}\n", idx + 1, response.code());
                }
            });
        }
    }
}
```