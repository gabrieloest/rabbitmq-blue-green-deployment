import pika
import os
import logging
import yaml
import rabbitmq_api_utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Loading blue configurations....')
with open("./config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

logger.info("Loading blue configurations...")
blue_rabbitmq = cfg['rabbitmq-blue']
blue_host = blue_rabbitmq['host']
blue_user = blue_rabbitmq['user']
blue_password = blue_rabbitmq['password']

logger.info('blue host: {}'.format(blue_host))
logger.info('blue user: {}'.format(blue_user))
logger.info('blue password: {}'.format(blue_password))

# Parse CLODUAMQP_URL (fallback to localhost)
blue_url = os.environ.get(
    'CLOUDAMQP_URL', 'amqp://{}:{}@{}/{}'.format(blue_user, blue_password,
                                                 blue_host, blue_user))
logger.info("Blue URL: {}".format(blue_url))

logger.info("Loading green configurations...")
green_rabbitmq = cfg['rabbitmq-green']
green_host = green_rabbitmq['host']
green_user = green_rabbitmq['user']
green_password = green_rabbitmq['password']

logger.info('green host: {}'.format(green_host))
logger.info('green user: {}'.format(green_user))
logger.info('green password: {}'.format(green_password))

# Parse CLODUAMQP_URL (fallback to localhost)
green_url = os.environ.get(
    'CLOUDAMQP_URL', 'amqp://{}:{}@{}/{}'.format(green_user, green_password,
                                                 green_host, green_user))
logger.info("Green URL: {}".format(green_url))

blue_rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(blue_host, blue_user,
                                                     blue_password)

green_rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(green_host, green_user,
                                                      green_password)

blue_json = blue_rmq_utils.export_definitions().json()

import_result = green_rmq_utils.import_definitions(blue_json)

logger.info("Import definitions from blue to green: {}".format(import_result))

all_queues_blue = blue_rmq_utils.get_all_queues()
queues_to_federate = list(filter(
    lambda item: ("deadletter" not in item["name"]),
    all_queues_blue.json()))

queue_name_vhost = dict((json["name"], json["vhost"])
                        for json in queues_to_federate)

vhosts = queue_name_vhost.values()
print("vhosts: {}".format(vhosts))

params = pika.URLParameters(green_url)
params.socket_timeout = 5
# Connect to CloudAMQP
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel

for item in vhosts:
    green_rmq_utils.create_federation_upstream(green_user, blue_url)
    green_rmq_utils.create_federation_policy(green_user)
