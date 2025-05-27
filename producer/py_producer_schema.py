from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import os

# Avro schema with integers
avro_schema_str = """
{
  "type": "record",
  "name": "Customer",
  "fields": [
    { "name": "first_name", "type": "string" },
    { "name": "last_name", "type": "string" },
    { "name": "zip_code", "type": "int" },
    { "name": "email", "type": "string" },
    { "name": "ssn", "type": "int" },
    { "name": "customer_id", "type": "int" }
  ]
}
"""

def dict_to_customer(obj, ctx):
    return obj

# Schema Registry config
schema_registry_conf = {
    'url': os.getenv('SCHEMA_REGISTRY_URL'),
    'basic.auth.user.info': f"{os.getenv('SCHEMA_REGISTRY_API_KEY')}:{os.getenv('SCHEMA_REGISTRY_API_SECRET')}"
}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(
    schema_registry_client=schema_registry_client,
    schema_str=avro_schema_str,
    to_dict=dict_to_customer
)

# Producer config
producer_conf = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer,
    'security.protocol': 'SASL_SSL',  # If using Confluent Cloud
    'sasl.mechanism': 'PLAIN'
}

print("BOOTSTRAP_SERVERS:", os.getenv('BOOTSTRAP_SERVERS'))
print("KAFKA_API_KEY", os.getenv('KAFKA_API_KEY'))
print("KAFKA_API_SECRET", os.getenv('KAFKA_API_SECRET'))
print("SCHEMA_REGISTRY_URL", os.getenv('SCHEMA_REGISTRY_URL'))
print("SCHEMA_REGISTRY_API_KEY", os.getenv('SCHEMA_REGISTRY_API_KEY'))
print("SCHEMA_REGISTRY_API_SECRET", os.getenv('SCHEMA_REGISTRY_API_SECRET'))

producer = SerializingProducer(producer_conf)

topic = os.getenv('TOPIC_NAME')
print(f"Producing to topic: {topic}")

customer_data = {
    "first_name": "Beth",
    "last_name": "Dutton",
    "zip_code": 94444,
    "email": "beth.dutton@yellowstone.com",
    "ssn": 223454667,
    "customer_id": 10017}

key = "customer-10017"

def delivery_callback(err, msg):
    if err:
        print(f'❌ Delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}]')

producer.produce(topic=topic, key=key, value=customer_data, on_delivery=delivery_callback)
producer.flush()
