import json
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitmqAPIUtils:

    headers = {'Content-type': 'application/json'}

    def __init__(self, host, user, password):
        self.user = user
        self.password = password
        self.url = 'https://{}/api/'.format(host)

    def get_all_queues(self):
        logger.info("Call RabbitMQ api... {}".format(self.url))
        url_method = self.url
        url_method += 'queues'
        r = requests.get(url_method, auth=(self.user, self.password))
        return r

    def is_queue_exists(self, vhost, queue):
        logger.info("Call RabbitMQ api...")
        logger.info("Verifying if queue {} exists...".format(queue))
        url_method = self.url
        url_method += ('queues/{}/{}'.format(vhost, queue))
        r = requests.get(url_method, auth=(self.user, self.password))
        return r.status_code == 200

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
