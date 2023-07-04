from flask import request, make_response
from flask_restful import Resource, reqparse
from flask_api import status
from miniagent import api
from miniagent.executer import ExecuterCaller

class Deposit(Resource):

    def post(self, account):

        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=int)
        args = parser.parse_args()
        
        data = dict(
            initial_param = dict(
                account = account ,
                amount = args['amount'],
            ),
            executer = 'banking.executer.deposit.Deposit',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return dict(message=rtn_message['message']), status_code
    
    def get(self, account):

        data = dict(
            initial_param = dict(
                account = account ,
            ),
            executer = 'banking.executer.deposit.DepositList',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)

        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return dict(message=rtn_message), status_code

class Raffle(Resource):

    def get(self, account):

        data = dict(
            initial_param = dict(
                account = account ,
            ),
            executer = 'banking.executer.raffle.Raffle',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_404_NOT_FOUND

        return rtn_message, status_code

class Event(Resource):

    def get(self):

        data = dict(
            executer = 'banking.executer.event.Event',
        )

        rtn, rtn_message = ExecuterCaller.instance().execute_command(data)
        
        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_404_NOT_FOUND

        return rtn_message, status_code

api.add_resource(Deposit, '/deposit/<string:account>', endpoint='deposit')
api.add_resource(Raffle, '/raffle/<string:account>', endpoint='raffle')
api.add_resource(Event, '/event', endpoint='event')
