from apscheduler.schedulers.background import BackgroundScheduler
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
        #invoices.send_invoices()
        ic = invoices.InvoiceCreator(['scheduler'])
        i=ic.send_invoices_customers(1)
        self.send_logs(i)
        return i

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
            self.send_invoices()



def run():    
    s=Scheduler(180)
    s.start(60*24)




