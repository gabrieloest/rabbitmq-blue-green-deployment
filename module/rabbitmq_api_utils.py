import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitmqAPIUtils:

    headers = {'Content-type': 'application/json'}

    def __init__(self, protocol, host, port, user, password):
        self.user = user
        self.password = password
        self.host = host
        self.url = '{}://{}:{}/api/'.format(protocol, host, port)

    def get_all_queues(self):
        logger.info("Call RabbitMQ api... {}".format(self.url))
        url_method = self.url
        url_method += 'queues'
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def get_queue_by_name(self, vhost, queue_name):
        url_method = self.url
        url_method += 'queues/{}/{}'.format(vhost, queue_name)
        logger.info("Call RabbitMQ api... {}".format(url_method))
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def is_queue_exists(self, vhost, queue):
        logger.info("Call RabbitMQ api...")
        logger.info("Verifying if queue {} exists...".format(queue))
        url_method = self.url
        url_method += ('queues/{}/{}'.format(vhost, queue))
        r = requests.get(url_method, auth=(self.user, self.password))
        return r.status_code == 200

    def export_definitions(self):
        logger.info("Call RabbitMQ api... {}".format(self.url))
        logger.info("Export definitions from host: {}".format(self.host))
        url_method = self.url
        url_method += 'definitions'
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def import_definitions(self, definitions):
        logger.info("Call RabbitMQ api...")
        logger.info("Export definitions to host: {}".format(self.host))
        url_method = self.url
        url_method += 'definitions'
        logger.info("Import definitions URL: {}".format(url_method))
        headers = {'Content-type': 'application/json'}
        logger.info("Importing definitions...")
        r = requests.post(url_method, auth=(self.user, self.password),
                         json=definitions, headers=headers)
        return r

    def create_federation_policy(self, vhost):
        logger.info("Call RabbitMQ api...")
        url_method = self.url
        url_method += ('policies/{}/federation'.format(vhost))
        logger.info("Create federation policy URL: {}".format(url_method))
        headers = {'Content-type': 'application/json'}
        data = {"pattern": '^(?!amq\\.).+',
                "definition": {"federation-upstream-set": "all"},
                "apply-to": "queues"}
        logger.info("Set queue policy DATA: {}".format(data))
        r = requests.put(url_method, auth=(self.user, self.password),
                         data=json.dumps(data), headers=headers)
        return r

    def create_federation_upstream(self, vhost, upstream_url):
        logger.info("Call RabbitMQ api...")
        url_method = self.url
        url_method += 'parameters/federation-upstream/{}/Federation'.format(vhost)
        logger.info("Create federation upstream URL: {}".format(url_method))
        headers = {'Content-type': 'application/json'}
        data = {"value": {"uri": upstream_url, "ack-mode": "on-confirm"}}
        logger.info("Create federation upstream DATA: {}".format(data))
        r = requests.put(url_method, auth=(self.user, self.password),
                         data=json.dumps(data), headers=headers)
        return r

    def create_shovel(self, vhost, src_queue, dest_queue, upstream_url, downstream_url):
        logger.info("Call RabbitMQ api...")
        url_method = self.url
        url_method += 'parameters/shovel/{}/shovel-{}'.format(vhost, src_queue)
        logger.info("Create shovel URL: {}".format(url_method))
        headers = {'Content-type': 'application/json'}
        data = {"value": {"src-protocol": "amqp091", "src-uri":  upstream_url,
                          "src-queue":  src_queue, "dest-protocol": "amqp091",
                          "dest-uri": downstream_url, "dest-queue": dest_queue}}
        logger.info("Create shovel DATA: {}".format(data))
        r = requests.put(url_method, auth=(self.user, self.password),
                         data=json.dumps(data), headers=headers)
        return r
