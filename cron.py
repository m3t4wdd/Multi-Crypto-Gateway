from models_db import Invoices, AvailableIndex
from backend import create_app
from database import db
from datetime import datetime, timezone, timedelta
from CheckPayments import CheckPayments as cp

app = create_app()

def cronlog(s):
    with open("./instance/cronjob.log", "a") as file:
        file.write(s + "\n")
        file.close()
# if the tx has been pending for at least 24 hours == expired
def is_expired(timestamp_str: str) -> bool:
    dt = datetime.fromisoformat(timestamp_str)  # parse time in ISO8601
    now = datetime.now(timezone.utc)           # current time in UTC
    return (now - dt) > timedelta(hours=1)


def check_invoices():
    with app.app_context():
        all_invoices = Invoices.query.all()
        for invoice in all_invoices:
            if invoice.status in ["pending", "detected"]:
                match invoice.coin_type:

                    case "BTC":
                        amount = cp.CheckOther(invoice.coin_type, invoice.address)
                        if amount > 0:
                            invoice.status = "paid"
                            invoice.amount = amount
                            db.session.commit()
                            cronlog(f"Bitcoin invoice {invoice.invoice_id} paid {amount}$")

                    case "XMR":
                        amount = cp.MoneroBalance(invoice.index)
                        if amount > 0:
                            invoice.status = "paid"
                            invoice.amount = amount
                            db.session.commit()
                            cronlog(f"Monero invoice: {invoice.invoice_id} paid {amount}")

                    case "LTC":
                        amount = cp.CheckOther(invoice.coin_type, invoice.address)
                        if amount > 0:
                            invoice.status = "paid"
                            invoice.amount = amount
                            db.session.commit()
                            cronlog(f"Litecoin invoice {invoice.invoice_id} paid {amount}$")

            #check for transactions expired within the last 24 hours
            if invoice.status in ["pending"]:

                if is_expired(str(invoice.expires_at)):
                    cronlog(f"invoice {invoice.invoice_id} expired")
                    
                    availableindex_index =  AvailableIndex(
                    index = invoice.index,
                    coin_type = invoice.coin_type
                    )
                    db.session.add(availableindex_index)
                    invoice.status = "expired"
                    db.session.commit()


if __name__ == "__main__":
    check_invoices()
