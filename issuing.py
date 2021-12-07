import invoices
from threading import Thread, Event
import time

# Modulo para fazer o scheduler

class Scheduler:
    def __init__(self):
        invoices.set_user(*invoices.get_login())
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
        finish=50
        t=time.time()
        while True:
            self.send_invoices()
            Event().wait(1)
            break
            #if time.time()-t >= finish:
            #    break
        self.reset_thread()
        return
        self.validate()


    # rodará por 24 horas a cada 3 horas
    # No final verifica se há transferências que não foram feitas
    def run(self):
        finish=3600*24
        finish=50
        t=time.time()
        time.time()-t>=finish
        while True:
            break
            self.send_invoices()
            Event().wait(1)
            break
            #if time.time()-t >= finish:
            #    break
        self.reset_thread()
        return
        self.validate()

    def reset_thread(self):
        self.thread=Thread(target=self.run)
    

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()
            return {'status': 'success', 'message': 'issuing started'}
        else:
            return {'status': 'fail', 'message': 'job already running'}




