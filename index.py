from flask import Flask, request, abort, jsonify
import starkbank
import invoices
import json

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({'user': str(invoices.starkbank.user.id)}) 


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method=='POST':
        r=invoices.webhook(request.json)
        return 'Sucess', 200
    else:
        abort(400)


invoices.set_user(*invoices.get_login())
invoices.create_webhook('https://project-starkbank.vercel.app/webhook')

if __name__=='__main__':
    app.run()

