import pika
import os
import logging
import time
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Loading configurations....')
with open("./config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

cluster = input("Please enter the cluste name: ")

rabbitmq = cfg[cluster]
host = rabbitmq['host']
user = rabbitmq['user']
password = rabbitmq['password']

logger.info('host: {}'.format(host))
logger.info('user: {}'.format(user))
logger.info('password: {}'.format(password))

# Parse CLODUAMQP_URL (fallback to localhost)
logger.info("Parse CLODUAMQP_URL (fallback to localhost)...")
url = os.environ.get(
    'CLOUDAMQP_URL', 'amqp://{}:{}@{}/{}'.format(user, password, host, user))
params = pika.URLParameters(url)
params.socket_timeout = 5


def message_process_function(channel, method, msg):
    print("Processing message...")
    # time.sleep(0.3)
    tag = method.delivery_tag
    print("Message {} processing finished".format(tag))
    channel.basic_ack(delivery_tag=tag)
    print("Message ack OK!")
    return


# Connect to CloudAMQP
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel

# create a function which is called on incoming messages


def callback(ch, method, properties, body):
    message_process_function(ch, method, body)


queue = input("Please enter queue name: ")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue)

# start consuming (blocks)
channel.start_consuming()
connection.close()
