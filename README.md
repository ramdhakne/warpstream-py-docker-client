# warpstream-py-docker-client
Py client for Warpstream Kafka Cluster. SR is dockerized to run locally. Client registers the schema with schema registry first and write record to the kafka cluster.

* TIP: Run the producer and consumer in two terminals so that consumer can be kept running and producer can be used to produce the records.

## Pre-requisties
* Create Warpsteam(WS) Kafka cluster 
* If using WS serverless then no need of creating agent for the broker
* Create WS Schema Registry (SR)

## Docker dir structure
```
/your-docker-dir/
├── .env                    # Environment variables for sensitive configs (e.g. API keys, schema registry URL)
├── Dockerfile              # Defines the container image for the consumer
├── docker-compose.yaml     # Compose file to run the consumer container
├── py_<client>.py          # Python consumer script (Avro + Schema Registry logic)
├── requirements.txt        # Python dependencies (confluent_kafka, etc.)
```

## Running the client
```docker-compose up --build```

### eg
```pwd```

```# producer```

```# producer % docker-compose up --build```

### Output should match like this
```
[+] Running 2/2
 ✔ producer                       Built                                                                                                                 0.0s 
 ✔ Container producer-producer-1  Recreated                                                                                                             0.1s 
Attaching to producer-1
producer-1  | BOOTSTRAP_SERVERS: serverless.warpstream.com:9092
producer-1  | KAFKA_API_KEY ccun_<redacted>
producer-1  | KAFKA_API_SECRET ccp_<redacted>
producer-1  | SCHEMA_REGISTRY_URL http://172.17.0.2:9094
producer-1  | SCHEMA_REGISTRY_API_KEY ccun_<redacted>
producer-1  | SCHEMA_REGISTRY_API_SECRET ccp_<redacted>
producer-1  | Producing to topic: ws_topic_1
producer-1  | ✅ Message delivered to ws_topic_1 [0]
producer-1 exited with code 0
```

### Running the dockerized SR agent 
```
docker run -p 9094:9094 public.ecr.aws/warpstream-labs/warpstream_agent:latest agent \
    -bucketURL file:test \
    -agentKey aks_00f6d8ed035055f534e81465b992eb82a3b04d00eff1f3661644c07ac3265000 \
    -region us-east-1 \
    -defaultVirtualClusterID vci_sr_911d8a6e_d28c_552c_c22a_00b344e37d11
```
