'''from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import invoices
import json

# Classe para programar o envio das faturas
class Scheduler:
    def __init__(self, interval):
        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(self.execute,'interval',minutes=interval, id='invoice_sender')
        self.scheduler=scheduler
        
    # inicia o scheduler
    def start(self, minutes):
        self.finish=datetime.now()+timedelta(0,60*minutes)
        self.scheduler.start()
        
    # encerra
    def shutdown(self):
        print('removendo')
        self.scheduler.remove_job('invoice_sender')
        self.scheduler.shutdown()

    def send_invoices(self):
        return send_invoices()

    def send_logs(self, invoices):
        with open(r'base\\invoices.json', 'r+') as o:
            data = json.load(o)
            for i in invoices:
                x={str(i.id):{'id': str(i.id),
                        'created': str(i.created)}}
            o.seek(0)
            json.dump(data, o, indent=4)

    def execute(self):
        if datetime.now()>=self.finish:
            self.shutdown()
        else:
            self.send_invoices()'''

import invoices
import json

def send_invoices():
    i = invoices.send_invoices(tags=['scheduler'])
    return i

def send_invoices():
    ic = invoices.InvoiceCreator(['teste_scheduler'])
    ic.send_invoices_customers(1)

# valida as transferências dos últimos 3 dias
def validate():
    tv=invoices.TransferValidator(3)
    tv.validate()

'''def run():    
    s=Scheduler(180)
    s.start(60*24)'''

import time
def run():
    while True:
        invoices.set_user(*invoices.get_login())
        send_invoices()
        time.sleep(120)





