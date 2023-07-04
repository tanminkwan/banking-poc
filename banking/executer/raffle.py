from miniagent.executer import ExecuterInterface
from banking.dbquery.queries import select_raffles

class Raffle(ExecuterInterface):

    def execute_command(self, 
                            initial_param: dict,
                        ) -> tuple[int, dict]:
        
        account = initial_param.get('account')
        reqs = select_raffles(account)

        results = []
        if reqs:

            for row in reqs:
            
                results.append(dict(
                    event_id     = row.event_id,
                    account      = row.account,
                    amount       = row.amount,
                    deposit_id   = row.deposit_id,
                    deposit_date = row.deposit_date,
                    created_date = row.created_date.isoformat()
                ))

        return 1 if results else 0, results