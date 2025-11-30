from database import db

class Invoices(db.Model):
    __tablename__ = "invoices"

    invoice_id = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    coin_type = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    index = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Text, nullable=False, default="pending")
    amount = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.Text, nullable=False)


class CoinIndex(db.Model):
    __tablename__ = "coin_index"

    id = db.Column(db.Integer, primary_key=True)
    coin_type = db.Column(db.Text, nullable=False, unique=True)
    last_index = db.Column(db.Integer, nullable=False, default=0)

class AvailableIndex(db.Model):
    __tablename__ = "reusable_index"

    id = db.Column(db.Integer, primary_key=True)
    coin_type = db.Column(db.Text, nullable=False, unique=True)
    index = db.Column(db.Integer, nullable=False)