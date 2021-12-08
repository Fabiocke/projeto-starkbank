import invoices

def test_login_api():
    expected = "4508183066312704"
    invoices.set_user(*invoices.get_login())
    result = invoices.starkbank.user.id
    result ==expected


def tests_the_invoice_is_being_generated_correctly_using_seed_42():
    invoices.set_user(*invoices.get_login())
    ic = invoices.InvoiceCreator(42)
    i1, i2 = ic.get_invoices_customers(2)
    assert (i1.amount, i1.fine, i1.interest, i1.tax_id, i1.name, i1.descriptions) == (41000, 2.8, 0.5, '154.814.600-50', 'Led', [{'key': '41000 balas.', 'value': 'R$41000,00'}])
    assert (i2.amount, i2.fine, i2.interest, i2.tax_id, i2.name, i2.descriptions) == (401300, 1.2, 0.3, '855.353.690-47', 'Maria', [{'key': '401300 balas.', 'value': 'R$401300,00'}])


def test_webhook_creator():
    webhook=invoices.create_webhook('https://teste')
    assert webhook.url=='https://teste'
    invoices.starkbank.webhook.delete(webhook.id)


def test_invoice_creator_using_seed_42():
    ic = invoices.InvoiceCreator(seed=42, tags=['test_invoice_creator'])
    i = ic.send_invoices_customers(1)[0]
    assert i.amount, i.name == (182500, "Led")
    invoices.starkbank.invoice.update(i.id, status="canceled")
    i=invoices.starkbank.invoice.get(i.id)
    assert i.status=='canceled'


