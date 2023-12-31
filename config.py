import os
from datetime import datetime, timedelta

#Service Port
PORT = 5000

#DEBUG
DEBUG = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')

import __main__
AGENT_NAME = os.environ.get('AGENT_NAME') or \
    os.path.basename(__main__.__file__).split('.')[0]

_roles_map_ = dict(
    bonnie         = "customer",
    clyde          = "customer",
    john_dillinger = "admin",
    event          = "service",
    raffle         = "service",
    deposit        = "service",
)

AGENT_ROLES  = os.environ.get('AGENT_ROLES') or _roles_map_.get(AGENT_NAME)

#
COMMAND_RECEIVER_ENABLED = os.getenv("COMMAND_RECEIVER_ENABLED", 'False').lower()\
      in ('true', '1', 't')
MESSAGE_RECEIVER_ENABLED = os.getenv("MESSAGE_RECEIVER_ENABLED").lower() in ('true', '1', 't') \
    if os.getenv("MESSAGE_RECEIVER_ENABLED") else AGENT_NAME=="raffle"

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

print("COMMAND_RECEIVER_ENABLED : ",str(COMMAND_RECEIVER_ENABLED))
print("MESSAGE_RECEIVER_ENABLED : ",str(MESSAGE_RECEIVER_ENABLED))
print("ZIPKIN_DOMAIN_NAME : ",ZIPKIN_DOMAIN_NAME)
print("ZIPKIN_PORT : ",ZIPKIN_PORT)
print("KAFKA_BOOTSTRAP_SERVERS : ",KAFKA_BOOTSTRAP_SERVERS)
print("ELASTIC_SEARCH_DOMAIN_NAME : ",ELASTIC_SEARCH_DOMAIN_NAME)
print("ELASTIC_SEARCH_PORT : ",ELASTIC_SEARCH_PORT)
print("DEPOSIT_SERVICE_ADDRESS : ",DEPOSIT_SERVICE_ADDRESS)
print("EVENT_SERVICE_ADDRESS : ",EVENT_SERVICE_ADDRESS)
print("RAFFLE_SERVICE_ADDRESS : ",RAFFLE_SERVICE_ADDRESS)
print("AGENT_NAME : ",AGENT_NAME)
print("AGENT_ROLES : ",AGENT_ROLES)

ZIPKIN_ADDRESS = (ZIPKIN_DOMAIN_NAME,int(ZIPKIN_PORT))

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, AGENT_NAME+'.db')

CUSTOM_MODELS_PATH = "banking.model"

CUSTOM_APIS_PATH = "banking.api"

KAFKA_BOOTSTRAP_SERVERS = KAFKA_BOOTSTRAP_SERVERS.split(',')

EXECUTERS_BY_TOPIC =\
[
    {"topic":"deposit."+AGENT_NAME.lower(),
    "executer":"banking.executer.deposit.ReadMessage",
    "agent_roles":["service"]},
]

SCHEDULER_TIMEZONE = "Asia/Seoul" 
SCHEDULER_API_ENABLED = True
EXIT_AFTER_JOBS = False
SCHEDULED_JOBS =\
[
    {
        "executer":"banking.executer.deposit.RequestDeposit",
        "trigger":"interval",
        "id":"request_deposit",
        "name":"Request Deposit",
        "minutes":1,
        "start_date":datetime.now()+timedelta(minutes=1),
#        "end_date":datetime.now()+timedelta(minutes=3),
        "agent_roles":["customer"],
    },
    {
        "executer":"banking.executer.event.CheckEvent",
        "trigger":"interval",
        "id":"check_event",
        "name":"Check Event",
        "seconds":30,
        "start_date":datetime.now()+timedelta(minutes=1),
#        "end_date":datetime.now()+timedelta(minutes=3),
        "agent_roles":["customer"],
    },
    {
        "executer":"banking.executer.event.CheckAmount",
        "trigger":"interval",
        "id":"check_amount",
        "name":"Check Amount",
        "seconds":30,
        "start_date":datetime.now()+timedelta(minutes=1),
        "agent_roles":["admin"],
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
C_ROLE = os.environ.get('X_ROLE') or ('tester' if AGENT_NAME=='bonnie' else 'customer')
