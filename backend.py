from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
import random, string, qrcode, base64
from io import BytesIO
from models_db import Invoices, CoinIndex, AvailableIndex
import generate_address as ga
from database import db


'''log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)'''

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()


SUPPORTED_COIN = ["BTC", "LTC", "XMR"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

def get_invoices_data(coin_type):
    invoice_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    coin_index = CoinIndex.query.filter_by(coin_type=coin_type).first() # instance of coin_index
    available = AvailableIndex.query.filter_by(coin_type=coin_type).first() # first available index (if exist)

    if available is not None:
        index = available.index
        row = db.session.get(AvailableIndex, available.id)
        db.session.delete(row)
        db.session.commit()
    else:
        index = coin_index.last_index + 1 # new index to use
        coin_index.last_index = index     # Update coin_index in db
        db.session.commit()

    
    if coin_type == "BTC":
        address = ga.generate_BTC(index)
    elif coin_type == "LTC":
        address = ga.generate_LTC(index)
    else:
        address = ga.generate_XMR(index)
        
    now = datetime.now(timezone.utc)  # UTC

    invoice =  Invoices(
        invoice_id = invoice_id,
        coin_type = coin_type,
        address = address,
        index = index,
        status = "pending",
        created_at = now.isoformat(),
        expires_at = (now + timedelta(hours=1)).isoformat()
    )
    db.session.add(invoice)
    db.session.commit()

    return invoice.invoice_id

def generate_qr(address: str):
    # Address QR Code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(address)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Convert in base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{qr_base64}"
    

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/create_invoice", methods=["GET"])
def create_invoice():
    coin = request.args.get("coin")
    if coin not in SUPPORTED_COIN:
        return "Coin type not valid or unsupported."
    
    if coin == "BTC":
        invoice_id = get_invoices_data("BTC")
        return redirect(url_for('invoice', invoice_id=invoice_id))
    
    if coin == "LTC":
        invoice_id = get_invoices_data("LTC")
        return redirect(url_for('invoice', invoice_id=invoice_id))
    
    if coin == "XMR":
        invoice_id = get_invoices_data("XMR")
        return redirect(url_for('invoice', invoice_id=invoice_id))

@app.route("/invoice/<invoice_id>")
def invoice(invoice_id):
    invoice = Invoices.query.filter_by(invoice_id=invoice_id).first()
    if invoice is None:
        return "Invoice id not valid"
    qr = generate_qr(invoice.address)
    return render_template("invoice.html", invoice=invoice, qr=qr)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
