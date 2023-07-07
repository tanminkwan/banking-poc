# banking-poc

## Apply docker compose

```
$ docker compose -f docker-compose-kafka.yml -f docker-compose-opensearch.yml -f docker-compose-zipkin.yml -f docker-compose.yml up -d
```

## Run kafka sink connector (to Opensearch)
```
echo '{"name":"opensearch-sink",
"config":{
"connector.class":"io.aiven.kafka.connect.opensearch.OpensearchSinkConnector",
"tasks.max":1,
"topics":"deposit.raffle",
"key.ignore":"true",
"connection.url":"http://172.17.0.1:9200",
"type.name":"log",
"schema.ignore":"true"
}
}'|curl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"
```

