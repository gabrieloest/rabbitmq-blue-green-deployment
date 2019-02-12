import pika
import os
import logging
import time
import config_resolver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cluster = input("Please enter the cluster name: ")

config = config_resolver.ConfigResolver(logger, cluster)
server_config = config.load_server_config()

logger.info("Parse URL ")
url = os.environ.get('URL', 'amqp://{}:{}@{}/{}'
                     .format(server_config['user'], server_config['password'],
                             server_config['host'], server_config['vhost']))

params = pika.URLParameters(url)
params.socket_timeout = 5


def message_process(channel, method, msg):
    print("Processing message...")
    time.sleep(1)
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
    message_process(ch, method, body)


queue = input("Please enter queue name: ")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queue)

# start consuming (blocks)
channel.start_consuming()
connection.close()
