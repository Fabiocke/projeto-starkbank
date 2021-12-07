from flask import Flask, request, abort, jsonify
import invoices
import issuing

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({'user': str(invoices.starkbank.user.id)}) 


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method=='POST':
        r=invoices.webhook(request.json)
        return 'Success', 200
    else:
        abort(400)


# Inicia o job de 24 horas
@app.route('/start_issuing')
def start_issuing():
    alive=scheduler.thread.is_alive()
    r=scheduler.start()
    return jsonify({**r, **{'alive':alive}})

@app.route('/get_scheduler')
def get_scheduler():
    return str(scheduler)


invoices.set_user(*invoices.get_login())
invoices.create_webhook('https://project-starkbank.vercel.app/webhook')
scheduler = issuing.Scheduler()

if __name__=='__main__':
    app.run()

