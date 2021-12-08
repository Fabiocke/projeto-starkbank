from datetime import datetime
import invoices
from threading import Thread, Event
import time

# Modulo para fazer o scheduler

# Decorador para retornar o log do ero


class Scheduler:
    def __init__(self):
        self.thread = Thread(target=self.run)

    def send_invoices(self):
        i = invoices.send_invoices(tags=['scheduler'])
        return i

    # valida as transferências dos últimos 3 dias
    def validate(self):
        tv=invoices.TransferValidator(3)
        v = tv.validate()
        return v

    # rodará por 24 horas a cada 3 horas
    # No final verifica se há transferências que não foram feitas
    def run(self):
        invoices.set_user(*invoices.get_login())
        print('start process...')
        finish=3600*24
        interval=3600*3
        t=time.time()
        while True:
            r=self.send_invoices()
            print(f'{len(r)} faturas emitidas em {str(datetime.now())}')
            Event().wait(interval)
            if time.time()-t >= finish:
                break
        self.reset_thread()
        self.validate()
        print('end process...')

    def reset_thread(self):
        self.thread=Thread(target=self.run)
    

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()
            return {'status': 'success', 'message': 'issuing started'}
        else:
            return {'status': 'fail', 'message': 'job already running'}



if __name__=='__main__':
    scheduler=Scheduler()
    scheduler.start()
    

