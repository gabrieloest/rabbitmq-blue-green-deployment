
# RabbitMQ Blue/Green Deployment

## About the project

## How it works?

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
git clone https://github.com/gabrieloest/rabbitmq-federation-utils
```
```
cd rabbitmq-federation-utils
```
```
python -m pip install -r requirements.txt
```
