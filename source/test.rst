Unittest
========



YAML
====
Get new API in Python YAML tag:
!python {model: account.invoice, id: account_invoice_customer0}: |
    self # is now a new api record
    assert (self.move_id), "Move falsely created at pro-forma"
