from miniagent import configure, db
from miniagent.executer import ExecuterInterface
from miniagent.adapters.kafka_producer import KafkaProducerAdapter
from miniagent.adapters.rest_caller import RESTCaller
from banking.dbquery.queries import insert_deposit, insert_raffle\
    , select_deposits

import uuid
import random
from datetime import datetime

def _get_url(agent_name:str):
    return configure.get('SERVICE_ENDPOINT').get(agent_name)

class RequestDeposit(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:
        
        account = configure.get('AGENT_NAME')

        amount = random.randint(1, 999) * 1000

        url = "http://"+_get_url('deposit')\
                 +"/deposit/"+account
        
        params={'amount':amount}

        return rest_caller.call_post(
                    url=url, 
                    json=params
                )
    
class Deposit(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict, 
                            producer: KafkaProducerAdapter,
                        ) -> tuple[int, dict]:
        
        topic = 'deposit.raffle'
        now =  datetime.now()

        message = dict(
            account = initial_param.get('account'),
            amount = initial_param.get('amount'),
            deposit_id = uuid.uuid4().hex,
            deposit_date = now.isoformat(),
        )

        insert_deposit(message)

        db.session.commit()

        return producer.produce_message(
            topic= topic,
            message= message
            )

class DepositList(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        account = initial_param.get('account')
        reqs = select_deposits(account)

        results = []
        if reqs:

            for row in reqs:
            
                results.append(dict(
                    account      = row.account,
                    amount       = row.amount,
                    deposit_id   = row.deposit_id,
                    deposit_date = row.deposit_date,
                    created_date = row.created_date.isoformat()
                ))

        return 1 if results else 0, {"results":results}

class ReadMessage(ExecuterInterface):

    def execute_command(self,
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        account = initial_param.get('account')
        amount = initial_param.get('amount')
        
        account_balance = amount + \
            (configure['C_BALANCE'][account] \
             if configure['C_BALANCE'].get(account) else 0)
        configure['C_BALANCE'][account] = account_balance

        tot_balance = configure['C_BALANCE']['total'] + amount
        configure['C_BALANCE']['total'] = tot_balance

        print("###### BALANCE : ", account, str(account_balance))
        print("###### BALANCE TOT : ", str(tot_balance))

        message = dict(
            account = account,
            amount = amount,
            deposit_id = initial_param.get('deposit_id'),
            deposit_date = initial_param.get('deposit_date'),
            event_id = "BOOM"
        )

        ACCOUNT_BOUND = 1000000
        TOTAL_BOUND = 10000000

        if account_balance >= ACCOUNT_BOUND and account_balance - amount < ACCOUNT_BOUND:
            message.update({"event_id":"EVENT_1M_BY_ACCOUNT"})
            insert_raffle(message)

        if tot_balance >= TOTAL_BOUND and tot_balance - amount < TOTAL_BOUND:
            message.update({"event_id":"EVENT_10M"})
            insert_raffle(message)

        db.session.commit()

        return 1, dict(message="Yummy")