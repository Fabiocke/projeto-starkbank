import invoices
import starkbank

def test_login_api():
    expected = "4508183066312704"
    invoices.set_user(*invoices.get_login())
    result = invoices.starkbank.user.id
    result ==expected


def tests_the_invoice_is_being_generated_correctly():
    ic = invoices.__name__InvoiceCreator(42)
    i1, i2 = ic.get_invoices_customers(2)
    assert (i1.amount, i1.fine, i1.interest, i1.tax_id, i1.name, i1.descriptions) == (450700, 1.2, 0.4, '993.920.040-44', 'Joãozinho', [{'key': '450700 balas.', 'value': 'R$450700,00'}])
    assert (i2.amount, i2.fine, i2.interest, i2.tax_id, i2.name, i2.descriptions) == (228700, 2.8, 0.2, '595.596.690-01', 'Goku', [{'key': '228700 balas.', 'value': 'R$228700,00'}])


