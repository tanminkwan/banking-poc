import os
from datetime import datetime, timedelta

#Service Port
PORT = 5000

#hosts
ZIPKIN_DOMAIN_NAME = os.environ.get('ZIPKIN_DOMAIN_NAME') or 'localhost'
ZIPKIN_PORT =  os.environ.get('ZIPKIN_DOMAIN_NAME') or '9411'
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS') or 'localhost:9092'
ELASTIC_SEARCH_DOMAIN_NAME = os.environ.get('ELASTIC_SEARCH_DOMAIN_NAME') or 'localhost'
ELASTIC_SEARCH_PORT = os.environ.get('ELASTIC_SEARCH_PORT') or '9200'
#custom service
FRONT_SERVICE_ADDRESS = os.environ.get('FRONT_SERVICE')
DEPOSIT_SERVICE_ADDRESS = os.environ.get('DEPOSIT_SERVICE_ADDRESS')
EVENT_SERVICE_ADDRESS = os.environ.get('EVENT_SERVICE_ADDRESS')
RAFFLE_SERVICE_ADDRESS = os.environ.get('RAFFLE_SERVICE_ADDRESS')

import __main__
AGENT_NAME = os.environ.get('AGENT_NAME') or \
    os.path.basename(__main__.__file__).split('.')[0]

ZIPKIN_ADDRESS = (ZIPKIN_DOMAIN_NAME,int(ZIPKIN_PORT))

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, AGENT_NAME+'.app.db')

CUSTOM_MODELS_PATH = "banking.model"

CUSTOM_APIS_PATH = "banking.api"

KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS.split(',')

EXECUTERS_BY_TOPIC =\
{
    "deposit."+AGENT_NAME.lower():
    "banking.executer.deposit.ReadMessage",
}