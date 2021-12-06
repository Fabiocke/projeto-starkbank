from ellipticcurve import privateKey
import starkbank
import json
import random
from datetime import datetime, timedelta

ENVIROMENT='sandbox'

ID_USER="4508183066312704"

ACCOUNT_ID = "20.018.183/0001-80"
ACCOUNT_NAME = "Stark Bank S.A."
ACCOUNT_BANK = "20018183"
ACCOUTN_BRANCH = "0001"
ACCOUNT_NUMBER = "6341320293482496"
ACCOUNT_TYPE = "payment"


# Classe usada para gerar as faturas
class InvoiceCreator:
    def __init__(self, seed=None, tags=[]):
        random.seed(seed)
        self.tags=tags
        
    # Busca a base de clientes
    def get_customers(self):
        with open('base\\customers.json') as o:
            return json.loads(o.read())
    
    # Seleciona n clientes aleatórios
    def get_random_customers(self, n):
        base = self.get_customers()
        choices = random.sample(list(base), n)
        return list(map(base.get, choices))
    
    # Gera uma fatura
    def get_invoice(self, customer):
        customer={'tax_id': customer['taxId'],
                 'name': customer['name']}
        amount=random.randint(1, 10000)*100
        data={'amount': amount,
        'fine': random.randint(5,30)/10,
        'interest': random.randint(1,15)/10,
        'tags':self.tags,
        'descriptions': [
                {
                    "key": f"{amount} balas.",
                    "value": f"R${amount},00"
                }
            ]}
            
        data = {**data, **customer}
        return starkbank.Invoice(**data)
    
    
    # Gera uma lista de faturas para uma lista de clientes
    def get_invoices(self, customers):
        invoices = list(map(self.get_invoice, customers))
        return invoices
    
    # Gera uma lista de faturas pra n clientes
    def get_invoices_customers(self, n):
        customers=self.get_random_customers(n)
        return self.get_invoices(customers)
    
    # Envia uma lista de faturas de n clinetes
    def send_invoices_customers(self, n):
        faturas=self.get_invoices_customers(n)
        invoices=starkbank.invoice.create(faturas)
        return invoices
    

# Instancia o usuário
def set_user(id_user, key):
    user = starkbank.Project( 
        environment = ENVIROMENT, 
        id = id_user , 
        private_key=key
    )
    starkbank.user=user


# envia de 8 a 12 faturas para clientes aleatórios
def send_invoices(seed=None, tags=[]):
    n = random.randint(8, 12)
    ic = InvoiceCreator(seed, tags)
    invoices = ic.send_invoices_customers(n)
    return invoices


# cria o webhook se não existir
def create_webhook(url):
    webhooks = starkbank.webhook.query()
    if url not in [i.url for i in webhooks]:
        starkbank.webhook.create( 
            url = url, 
            subscriptions = [ "invoice" ])



# transfere o valor recebido
def set_transfer(amount, id_log):
    transfers = starkbank.transfer.create([
        starkbank.Transfer(
            amount=amount,
            tax_id=ACCOUNT_ID,
            name=ACCOUNT_NAME,
            bank_code=ACCOUNT_BANK,
            branch_code=ACCOUTN_BRANCH,
            account_number=ACCOUNT_NUMBER,
            account_type=ACCOUNT_TYPE,
            tags=["invoice", id_log]
        )
    ])
    return transfers[0]


# recebe os resultados do webhook e registra
def webhook(req):
    if req['event']['subscription']!='invoice':
        return
    type_log=req['event']['log']['type']
    id_log=req['event']['log']['id']
    invoice=req['event']['log']['invoice']
    amount = invoice['amount']-invoice['fee']
    id_invoice = invoice['id']
    
    if type_log=='credited':
        transfer = set_transfer(amount, id_log)
    else:
        transfer={}
    register_transfer(id_log, type_log, id_invoice, transfer.id, 'webhook')


# registra a transferência na base:
def register_transfer(id_log, type_log, id_invoice, id_transfer, origin):
    transfer={'id':id_transfer,
                'datetime': str(datetime.now()),
                'id_log':id_log,
                'type_log':type_log,
                'id_invoice':id_invoice,
                'origin':origin}

    with open(r'base\\transfers.json', 'r+') as o:
        data = json.load(o)
        data.update({str(id_transfer):transfer})
        o.seek(0)
        json.dump(data, o, indent=4)



# Verifica se todos os valores foram transferidos automaticamente pelo webhook pros últimos "days" dias, e transfere os que não foram feitos
class TransferValidator:
    def __init__(self, days):
        self.days=days
    
    # Busca os ids dos logs das faturas que foram creditadas
    def get_credited_invoices_log_id(self, after, before):
        logs = starkbank.invoice.log.query(
            after=after,
            before=before,
            limit=None
        )

        return [i for i in logs]
        return [log.id for log in logs if log.type=='credited']
    
    # Retorna os logs das fasturas que foram creditadas e transferidas
    def get_invoices_transfers(self, after, before):
        transfers = starkbank.transfer.query(
            after=after,
            before=before
        )

        invoices_transfers = [i.tags[1] for i in transfers if 'invoice' in i.tags]
        return invoices_transfers
    
    
    # Retorna os logs que não tiveram a transferência realizada
    def check_transfers(self):
        after=(datetime.now()-timedelta(self.days)).strftime('%Y-%m-%d')
        before=datetime.now().strftime('%Y-%m-%d')
        
        credited=self.get_credited_invoices_log_id(after, before)
        logs_credited=[log for log in credited if log.type=='credited']
        logs_transferred=self.get_invoices_transfers(after, before)
        pendency=[i for i in logs_credited if i.id not in logs_transferred]
        return pendency
    
    # Realiza a transferência
    def transfer(self, log):
        amount=log.invoice.amount-log.invoice.fee
        transfer = set_transfer(amount, log.id)
        register_transfer(log.id, log.type, log.invoice.id, transfer.id, 'robot')
    
    # validar e transferir
    def validate(self):        
        logs=self.check_transfers()
        for log in logs:
            self.transfer(log)



# checa os créditos dos últimos 3 dias e transfere caso não tenha sido transferido 
def validatin_transfers():
    tv=TransferValidator(3)
    tv.validate()


# retorna o id e private key
def get_login():
    with open('privateKey.pem') as o:
        PRIVATE_KEY = o.read()
        return ID_USER, PRIVATE_KEY



if __name__=="__main__":
    
    set_user(*get_login())
    #ic = InvoiceCreator(tags=['Teste'])
    #invoices = ic.send_invoices_customers(1)
    tv=TransferValidator(3)
    print(tv.check_transfers())
    #print(send_invoices(['Teste']))



