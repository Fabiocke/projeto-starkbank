from flask import Flask, request, abort, jsonify
import starkbank
import invoices
import json

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({'user': str(invoices.starkbank.user)}) 


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method=='POST':
        req = json.dumps(request.json)
        r=invoices.webhook(req)
        return 'Sucess', 200
    else:
        abort(400)
        

invoices.set_user()
invoices.create_webhook('https://project-starkbank.vercel.app/webhook')
