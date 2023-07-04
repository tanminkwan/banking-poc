from banking.model.models import Deposit, Raffle
from sqlalchemy import or_
from sqlalchemy.sql import insert, update
from miniagent import db
from datetime import datetime

def insert_deposit(data: dict):

    insert_dict = data.copy()
    insert_dict.update(dict(
        created_date = datetime.now()
    ))
    stmt = insert(Deposit).values(**insert_dict)
    db.session.execute(stmt)

def insert_raffle(data: dict):

    insert_dict = data.copy()
    insert_dict.update(dict(
        created_date = datetime.now()
    ))
    stmt = insert(Raffle).values(**insert_dict)
    db.session.execute(stmt)

def select_raffles(account: str):

    reqs = Raffle.query\
        .filter(or_(Raffle.account == account, account=='all')).all()
    
    return reqs

def select_deposits(account: str):

    reqs = Deposit.query\
        .filter(or_(Deposit.account == account, account=='all')).all()
    
    return reqs