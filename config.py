import os
from datetime import datetime, timedelta

#Service Port
PORT = 5000

#DEBUG
DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')

#hosts
ZIPKIN_DOMAIN_NAME = os.environ.get('ZIPKIN_DOMAIN_NAME') or 'localhost'
ZIPKIN_PORT =  os.environ.get('ZIPKIN_PORT') or '9411'
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS') or 'localhost:9092'
ELASTIC_SEARCH_DOMAIN_NAME = os.environ.get('ELASTIC_SEARCH_DOMAIN_NAME') or 'localhost'
ELASTIC_SEARCH_PORT = os.environ.get('ELASTIC_SEARCH_PORT') or '9200'
#custom service
DEPOSIT_SERVICE_ADDRESS = os.environ.get('DEPOSIT_SERVICE_ADDRESS') or 'localhost:5011'
EVENT_SERVICE_ADDRESS = os.environ.get('EVENT_SERVICE_ADDRESS') or 'localhost:5012'
RAFFLE_SERVICE_ADDRESS = os.environ.get('RAFFLE_SERVICE_ADDRESS') or 'localhost:5013'

import __main__
AGENT_NAME = os.environ.get('AGENT_NAME') or \
    os.path.basename(__main__.__file__).split('.')[0]

print("ZIPKIN_DOMAIN_NAME : ",ZIPKIN_DOMAIN_NAME)
print("ZIPKIN_PORT : ",ZIPKIN_PORT)
print("KAFKA_BOOTSTRAP_SERVERS : ",KAFKA_BOOTSTRAP_SERVERS)
print("ELASTIC_SEARCH_DOMAIN_NAME : ",ELASTIC_SEARCH_DOMAIN_NAME)
print("ELASTIC_SEARCH_PORT : ",ELASTIC_SEARCH_PORT)
print("DEPOSIT_SERVICE_ADDRESS : ",DEPOSIT_SERVICE_ADDRESS)
print("EVENT_SERVICE_ADDRESS : ",EVENT_SERVICE_ADDRESS)
print("RAFFLE_SERVICE_ADDRESS : ",RAFFLE_SERVICE_ADDRESS)
print("AGENT_NAME : ",AGENT_NAME)

ZIPKIN_ADDRESS = (ZIPKIN_DOMAIN_NAME,int(ZIPKIN_PORT))

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, AGENT_NAME+'.db')

CUSTOM_MODELS_PATH = "banking.model"

CUSTOM_APIS_PATH = "banking.api"

KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS.split(',')

EXECUTERS_BY_TOPIC =\
{
    "deposit."+AGENT_NAME.lower():
    "banking.executer.deposit.ReadMessage",
}

SCHEDULER_TIMEZONE = "Asia/Seoul" 
SCHEDULED_JOBS =\
[
    {
        "executer":"banking.executer.deposit.RequestDeposit",
        "trigger":"interval",
        "id":"request_deposit",
        "name":"Request Deposit",
        "minutes":2,
        "start_date":datetime.now()+timedelta(minutes=1),
        "agents":["bonnie","clyde"]
    },
    {
        "executer":"banking.executer.event.CheckEvent",
        "trigger":"interval",
        "id":"check_event",
        "name":"Check Event",
        "minutes":3,
        "start_date":datetime.now()+timedelta(minutes=1),
        "agents":["bonnie","clyde"]
    },
    {
        "executer":"banking.executer.event.CheckAmount",
        "trigger":"interval",
        "id":"check_amount",
        "name":"Check Amount",
        "minutes":4,
        "start_date":datetime.now()+timedelta(minutes=1),
        "agents":["john_dillinger"]
    },
]

SERVICE_ENDPOINT =\
{
    "deposit":DEPOSIT_SERVICE_ADDRESS+"/api/v1",
    "event":EVENT_SERVICE_ADDRESS+"/api/v1",
    "raffle":RAFFLE_SERVICE_ADDRESS+"/api/v1",
}

#Custom defined valuables
C_BALANCE = {"total":0}