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

# retorna o json de transferências
@app.route('/get_transfers')
def get_transfers():
    with open('base\\transfers.json') as o:
        data=json.loads(o.read())
        return jsonify(data)

# retorna as chaves
def get_keys():
    with open('keys.json') as o:
        data=json.loads(o.read())
        return data['ID_USER'], data['PRIVATE_KEY']

invoices.set_user(*get_keys())
invoices.create_webhook('https://project-starkbank.vercel.app/webhook')

if __name__=='__main__':
    app.run()

