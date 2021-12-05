from flask import Flask, request, abort
import invoices
import json

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method=='POST':
        req = json.dumps(request.json)
        r=invoices.webhook(req)
        return 'Sucess', 200
    else:
        abort(400)
        

if __name__=='__main__':
    invoices.set_user()
    invoices.create_webhook('project-starkbank.vercel.app\webhook')
