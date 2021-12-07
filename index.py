from flask import Flask, request, abort, jsonify
import invoices
import issuing

app = Flask(__name__)

# Decorador para retornar o log do ero
import traceback
def log_erro(f):
    def func_erro(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return {'status': 'erro', 'log': traceback.format_exc()}, 400

    return func_erro


@app.route('/')
def home():
    return jsonify({'user': str(invoices.starkbank.user.id)}), 200


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method=='POST':
        r=invoices.webhook(request.json)
        return 'Success', 200
    else:
        abort(400)


# Inicia o job de 24 horas
@app.route('/start_issuing')
@log_erro
def start_issuing():
    ic = invoices.InvoiceCreator(tags=['teste_scheduler1'])
    r = ic.send_invoices_customers(1)
    return str(r)
    r=scheduler.start()
    return jsonify({**r}), 200



invoices.set_user(*invoices.get_login())
invoices.create_webhook('https://project-starkbank.vercel.app/webhook')
scheduler = issuing.Scheduler()




if __name__=='__main__':
    app.run()

