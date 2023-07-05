from miniagent import configure
from miniagent.executer import ExecuterInterface
from miniagent.adapters.rest_caller import RESTCaller

class Event(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:
        
        account = configure.get('AGENT_NAME')

        url = "http://"+configure.get('SERVICE_ENDPOINT').get('raffle')+"/raffle/all"
        
        status, result = rest_caller.call_get(url=url)

        for row in result.get('results'):
            
            descriptions = dict(
                EVENT_10M_BY_ACCOUNT = "## {}님의 입금액이 천만원을 넘었습니다. 상금으로 2천만원을 드립니다.".format(row['account']),
                EVENT_100M = "## {}님의 입금으로 KDB산업은행 총 입금액이 1억원을 돌파하였습니다. 상금으로 2억원을 드립니다.".format(row['account']),
                EVENT_1M_BY_ACCOUNT = "## {}님의 입금액이 100만원을 넘었습니다. 상금으로 200만원을 드립니다.".format(row['account']),
                EVENT_10M = "## {}님의 입금으로 KDB산업은행 총 입금액이 천만원을 돌파하였습니다. 상금으로 2천만원을 드립니다.".format(row['account']),
            )
            row.update(dict(
                description = descriptions[row.get('event_id')] if descriptions.get(row.get('event_id')) else "Expired Event"
            ))

        return status, result

class CheckEvent(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                            rest_caller: RESTCaller,
                        ) -> tuple[int, dict]:
        
        url = "http://"+configure.get('SERVICE_ENDPOINT').get('event')+"/event"
        
        return rest_caller.call_get(url=url)