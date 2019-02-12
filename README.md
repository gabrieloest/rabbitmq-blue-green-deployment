
# RabbitMQ Blue/Green Deployment

## About the project
The objective of this project, is to make easy do major upgrades of RabbitMq version. Major upgrade refers to upgrading a RabbitMQ release from one version to another, with known compatibility side effects between the two versions. To do that, this project use the **blue/green** strategy, automatizing all the steps needed.

## What is blue/green deployment?
Blue-green deployment is an upgrade strategy that is based on the idea of to setting up a second RabbitMQ cluster (the "green" one) next to the current production cluster (the "blue" one). Applications are then switched to the "green" cluster. When that migration is done, the "blue" cluster is decomissioned (shut down).

## How it works?
1. Deploy a brand new cluster(green) - Manually
2. Importing definitions - Script
3. Configuring Queue Federation - Script
    1. Define the upstream on "green" and point it to "blue"
    2. Define a policy matching all queues which configure blue as the upstream
4. Switch consumers - Manually
5. Draining messages - Script
5. Switch producers - Manually

## Configuration
1. Create file `config/config.yml` with the following content:
```
rabbitmq-blue:
  protocol:
  host:
  user:
  password:
  vhost:

rabbitmq-green:
  protocol:
  host:
  user:
  password:
  vhost:
```
2. Fill the fields with the values to access your RabbitmMQ server

## Usage
```
git clone https://github.com/gabrieloest/rabbitmq-blue-green-deployment
```
```
cd rabbitmq-blue-green-deployment
```
```
python -m pip install -r requirements.txt
```

After deploy the brand new cluster, execute `blue_green.py` script:
```
python module/federation.py
```
