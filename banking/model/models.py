from miniagent import db

class Deposit(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable=False)
   deposit_id = db.Column(db.String(100), nullable=False)   
   account = db.Column(db.String(100), nullable=False)
   amount = db.Column(db.Integer, nullable=False)
   deposit_date = db.Column(db.String(100), nullable=False)
   created_date = db.Column(db.DateTime())

class Raffle(db.Model):
   id = db.Column(db.Integer, primary_key = True, nullable=False)
   event_id = db.Column(db.String(100), nullable=False)   
   deposit_id = db.Column(db.String(100), nullable=False)   
   account = db.Column(db.String(100), nullable=False)
   amount = db.Column(db.Integer, nullable=False)
   deposit_date = db.Column(db.String(100), nullable=False)
   created_date = db.Column(db.DateTime())