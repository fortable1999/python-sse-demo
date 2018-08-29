## Introduction
 to be continued

## Architecture
```
User
 O (Hi!)                  +---------+
-+-     ------------------| Browser |
 |                        +---------+
| |                            |                User
                               v              ============
                          +----------+          SSED service
                          | Balancer |
                          +----------+
                               v(:80)
                          +----------+
                          |  Nginx   |
                          +----------+
                           /         \
                           v(:5001)  v(:5002)
                  +--------+        +--------+
                  |  web   |        |  ssed  |
                  +--------+        +--------+
                      |  |               |
                      |  +------------+  |
                      |               |  |
                      v(:9200)        v  v(:9092)
                  +--------+        +--------+    (:2181)+--------+
                  |  es     |       | kafka  |---------->| zk     |
                  +--------+        +--------+           +--------+
                      A               A  
                      |  +------------+  
                      |  |               
                      |  |               
                  +--------+        +--------+
                  |logstash|        | consul |
                  +--------+        +--------+
                       A(:5044)          |        SSED service
                       |                 v     =============
                  +----------+      +--------+    Web servers
                  | filebeat |<---- | confd  |
                  +----------+      +--------+
                       A
                       |
                  +----------+      +--------+
                  | log files|<---- | httpd  |
                  +----------+      +--------+



```

## How to use

### Build the image
```docker-compose build```

### Start service
```docker-compose up```

### Shutdown service
```docker-compose stop```

### Delete files
```docker-compose rm```

