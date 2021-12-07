import invoices
from threading import Thread
import time

# Modulo para fazer o scheduler

class Scheduler:
    def __init__(self):
        self.thread = Thread(target=self.run)

    def send_invoices(self):
        i = invoices.send_invoices(tags=['scheduler'])
        return i

    def send_invoices(self):
        ic = invoices.InvoiceCreator(tags=['teste_scheduler'])
        ic.send_invoices_customers(1)

    # valida as transferências dos últimos 3 dias
    def validate(self):
        tv=invoices.TransferValidator(3)
        v = tv.validate()
        return v

    # rodará por 24 horas a cada 3 horas
    # No final verifica se há transferências que não foram feitas
    def run(self):
        finish=3600*24
        finish=60*1.5
        t=time.time()
        while True:
            time.sleep(5)
            break
            invoices.set_user(*invoices.get_login())
            self.send_invoices()
            time.sleep(60)
            if time.time()-t >= finish:
                break
        self.thread=Thread(target=self.run)
        return
        self.validate()


    def start(self):
        if not self.thread.is_alive():
            self.thread.start()
            return {'status': 'success', 'message': 'issuing started'}
        else:
            return {'status': 'fail', 'message': 'job already running'}




