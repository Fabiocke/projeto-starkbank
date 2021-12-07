import invoices
from threading import Thread
import time

def send_invoices():
    i = invoices.send_invoices(tags=['scheduler'])
    return i

def send_invoices():
    ic = invoices.InvoiceCreator(tags=['teste_scheduler'])
    ic.send_invoices_customers(1)

# valida as transferências dos últimos 3 dias
def validate():
    tv=invoices.TransferValidator(3)
    v = tv.validate()
    return v

# rodará por 24 horas a cada 3 horas
def run():
    finish=3600*24
    finish=60*5
    t=time.time()
    while time.time()-t <= finish:
        invoices.set_user(*invoices.get_login())
        send_invoices()
        print(1)
        time.sleep(120)
    print(validate())

thread=Thread(target=run)

def start():
    if not thread.is_alive():
        thread.start()
        return {'status': 'success', 'message': 'issuing started'}
    else:
        return {'status': 'fail', 'message': 'thread already running'}




