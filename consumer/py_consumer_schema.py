from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka import Consumer
import sys
import os

# Kafka config
kafka_config = {
    'group.id': 'python-avro-consumer-group',
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'sasl.username': os.getenv('KAFKA_API_KEY'),
    'sasl.password': os.getenv('KAFKA_API_SECRET'),
    'security.protocol': 'SASL_SSL',  # If using Confluent Cloud
    'sasl.mechanism': 'PLAIN',
    'auto.offset.reset': 'earliest'
}

print("BOOTSTRAP_SERVERS:", os.getenv('BOOTSTRAP_SERVERS'))
print("KAFKA_API_KEY", os.getenv('KAFKA_API_KEY'))
print("KAFKA_API_SECRET", os.getenv('KAFKA_API_SECRET'))
print("SCHEMA_REGISTRY_URL", os.getenv('SCHEMA_REGISTRY_URL'))
print("SCHEMA_REGISTRY_API_KEY", os.getenv('SCHEMA_REGISTRY_API_KEY'))
print("SCHEMA_REGISTRY_API_SECRET", os.getenv('SCHEMA_REGISTRY_API_SECRET'))

# Schema Registry config
schema_registry_conf = {
    'url': os.getenv('SCHEMA_REGISTRY_URL'),
    'basic.auth.user.info': f"{os.getenv('SCHEMA_REGISTRY_API_KEY')}:{os.getenv('SCHEMA_REGISTRY_API_SECRET')}"
}

# Initialize Schema Registry Client
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Define the Avro schema as used by the producer
avro_schema_str = """
{
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "first_name", "type": "string"},
    {"name": "last_name", "type": "string"},
    {"name": "zip_code", "type": "int"},
    {"name": "email", "type": "string"},
    {"name": "ssn", "type": "int"},
    {"name": "customer_id", "type": "int"}
  ]
}
"""

# Define deserializers
key_deserializer = StringDeserializer('utf_8')
value_deserializer = AvroDeserializer(
    schema_registry_client=schema_registry_client,
    schema_str=avro_schema_str
)

# Create Kafka consumer
consumer = Consumer(kafka_config)
topic = os.getenv('TOPIC_NAME')  # Replace with your topic
consumer.subscribe([topic])

print(f"Consuming from topic: {topic}")

try:
    while True:
        msg = consumer.poll(1.0)  # Wait for message
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        key = key_deserializer(msg.key(), SerializationContext(msg.topic(), MessageField.KEY))
        value = value_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

        print(f"Received message: Key={key}, Value={value}")

except KeyboardInterrupt:
    print("Stopping consumer...")

finally:
    consumer.close()
