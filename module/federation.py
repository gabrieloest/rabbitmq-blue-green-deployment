import os
import logging
import rabbitmq_api_utils
import config_resolver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

blue_config = config_resolver.ConfigResolver(logger, 'blue')
blue_server_config = blue_config.load_server_config()

blue_url = os.environ.get('URL', 'amqp://{}:{}@{}'
                          .format(blue_server_config['user'],
                                  blue_server_config['password'],
                                  blue_server_config['host']))

logger.info("Blue URL: {}".format(blue_url))

green_config = config_resolver.ConfigResolver(logger, 'blue')
green_server_config = green_config.load_server_config()

green_url = os.environ.get('URL', 'amqp://{}:{}@{}'
                           .format(green_server_config['user'],
                                   green_server_config['password'],
                                   green_server_config['host']))

logger.info("Green URL: {}".format(green_url))

blue_rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(blue_server_config['host'],
                                                     blue_server_config['user'],
                                                     blue_server_config['password'])

green_rmq_utils = rabbitmq_api_utils.RabbitmqAPIUtils(green_server_config['host'],
                                                      green_server_config['user'],
                                                      green_server_config['password'])

blue_definitions_json = blue_rmq_utils.export_definitions().json()

import_result = green_rmq_utils.import_definitions(blue_definitions_json)

logger.info("Import definitions from blue to green: {}".format(import_result))

all_queues_blue = blue_rmq_utils.get_all_queues()
queues_to_federate = list(filter(
    lambda item: ("deadletter" not in item["name"]),
    all_queues_blue.json()))

queue_name_vhost = dict((json["name"], json["vhost"])
                        for json in queues_to_federate)

vhosts = queue_name_vhost.values()
print("vhosts: {}".format(vhosts))

for item in vhosts:
    green_rmq_utils.create_federation_upstream(item, blue_url)
    green_rmq_utils.create_federation_policy(item)
